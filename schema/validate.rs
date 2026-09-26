//! Execute the schema and fixture transactions against EDB's in-memory engine.
//! The harness writes no database, contacts no service, and uses no credentials.
use edb_core::edn::write_edn;
use edb_core::edn_pull::parse_pull_edn;
use edb_core::edn_query::{EdnQueryArgument, parse_query_edn};
use edb_core::edn_value::value_to_edn;
use edb_core::{Database, Keyword, QueryControl, QueryResult, QuerySourceValue, QueryValue, Value};
use std::collections::{BTreeMap, BTreeSet};
use std::error::Error;
use std::path::{Path, PathBuf};

type Result<T> = std::result::Result<T, Box<dyn Error>>;

fn require(condition: bool, message: &str) -> Result<()> {
    if !condition {
        return Err(message.into());
    }
    Ok(())
}

fn query(database: &Database, text: &str) -> Result<Vec<Vec<QueryValue>>> {
    let query = parse_query_edn(text)?;
    let bound = query.bind(&[EdnQueryArgument::Source(QuerySourceValue::Database(
        database.database_value(),
    ))])?;
    match bound.execute(&QueryControl::default(), None)?.result {
        QueryResult::Relation(rows) => Ok(rows),
        _ => Err("expected a relation query result".into()),
    }
}

fn entity_id(value: &QueryValue) -> Result<u64> {
    match value {
        QueryValue::Scalar(Value::Ref(id)) => Ok(*id),
        QueryValue::Scalar(Value::Long(id)) if *id >= 0 => Ok(*id as u64),
        _ => Err(format!("expected an entity ID, got {value:?}").into()),
    }
}

fn attribute(database: &Database, namespace: &str, name: &str) -> Result<u32> {
    let id = database
        .entid(&Keyword::new(namespace, name))
        .ok_or_else(|| format!("missing attribute :{namespace}/{name}"))?;
    Ok(id.try_into()?)
}

fn edn(value: &Value) -> Result<String> {
    Ok(write_edn(&value_to_edn(value)?)?)
}

fn install(database: &Database, path: &Path, instant: i64) -> Result<Database> {
    let text = std::fs::read_to_string(path)?;
    let report = database
        .with_edn(&text, instant)
        .map_err(|error| format!("{}: {error}", path.display()))?;
    println!(
        "PASS {} ({} datoms, basis {})",
        path.file_name().unwrap().to_string_lossy(),
        report.tx_data.len(),
        report.db_after.basis_t()
    );
    Ok(report.db_after)
}

fn expect_rejected(database: &Database, label: &str, transaction: &str, code: &str) -> Result<()> {
    match database.with_edn(transaction, 10_000) {
        Ok(_) => Err(format!("{label}: invalid transaction unexpectedly succeeded").into()),
        Err(error) if error.code == code => {
            println!("PASS reject {label} ({})", error.code);
            Ok(())
        }
        Err(error) => Err(format!("{label}: expected {code}, got {error}").into()),
    }
}

fn check_readback(database: &Database) -> Result<()> {
    let rows = query(database, "[:find ?e ?id :where [?e :entity/id ?id]]")?;
    require(
        rows.len() >= 2,
        "fixtures must contain at least two UUID entities",
    )?;
    let pattern = parse_pull_edn("[:db/id :entity/id {:entity/kinds [:db/ident]}]")?;
    for row in &rows {
        let entity = entity_id(&row[0])?;
        let pulled = database.pull(&pattern, entity)?;
        let QueryValue::Map(ref entries) = pulled else {
            return Err("Pull did not return a map".into());
        };
        let key = QueryValue::Scalar(Value::Keyword(Keyword::new("entity", "id")));
        require(
            entries.iter().any(|(k, v)| k == &key && v == &row[1]),
            "Pull UUID did not match Datalog readback",
        )?;
    }
    let kinds = query(
        database,
        "[:find ?e ?kind :where [?e :entity/id _] [?e :entity/kinds ?kind]]",
    )?;
    require(!kinds.is_empty(), "fixtures must have entity kinds")?;
    for row in &rows {
        require(
            kinds.iter().any(|kind_row| kind_row[0] == row[0]),
            "every UUID entity must have a declared kind",
        )?;
    }
    let required_attributes = attribute(database, "db.entity", "attrs")?;
    let mut ensures = String::from("[");
    for row in &kinds {
        require(
            !database
                .values(entity_id(&row[1])?, required_attributes)
                .is_empty(),
            "every declared kind must have a nonempty entity spec",
        )?;
        ensures.push_str(&format!(
            "[:db/ensure {} {}]",
            entity_id(&row[0])?,
            entity_id(&row[1])?
        ));
    }
    ensures.push(']');
    database.with_edn(&ensures, 9_000)?;
    println!(
        "PASS Datalog/Pull readback of {} entities and {} explicit entity-spec checks",
        rows.len(),
        kinds.len()
    );
    Ok(())
}

fn expect_count(database: &Database, label: &str, text: &str, expected: usize) -> Result<()> {
    let rows = query(database, text)?;
    require(
        rows.len() == expected,
        &format!("{label}: expected {expected} rows, got {}", rows.len()),
    )?;
    println!("PASS {label}");
    Ok(())
}

struct PlacementGraph {
    parents: BTreeMap<u64, Vec<u64>>,
    lessons: BTreeSet<u64>,
    questions: BTreeSet<u64>,
}

impl PlacementGraph {
    fn read(database: &Database) -> Result<Self> {
        let mut parents: BTreeMap<u64, Vec<u64>> = BTreeMap::new();
        for row in query(
            database,
            "[:find ?parent ?child :where [?p :placement/parent ?parent] [?p :placement/content ?child]]",
        )? {
            parents
                .entry(entity_id(&row[1])?)
                .or_default()
                .push(entity_id(&row[0])?);
        }
        let entities_of_kind = |kind: &str| -> Result<BTreeSet<u64>> {
            query(
                database,
                &format!("[:find ?e :where [?e :entity/kinds :kind/{kind}]]"),
            )?
            .iter()
            .map(|row| entity_id(&row[0]))
            .collect()
        };
        Ok(Self {
            parents,
            lessons: entities_of_kind("lesson")?,
            questions: entities_of_kind("question")?,
        })
    }

    fn ancestors(&self, child: u64) -> BTreeSet<u64> {
        let mut seen = BTreeSet::new();
        let mut pending = self.parents.get(&child).cloned().unwrap_or_default();
        while let Some(parent) = pending.pop() {
            if seen.insert(parent) {
                pending.extend(self.parents.get(&parent).into_iter().flatten().copied());
            }
        }
        seen
    }
}

fn single_ref(database: &Database, entity: u64, attr: u32, label: &str) -> Result<u64> {
    let values = database.values(entity, attr);
    match values.as_slice() {
        [Value::Ref(id)] => Ok(*id),
        _ => Err(format!("app/question-ownership: {entity} must have one {label}").into()),
    }
}

// This is an application-level content check. EDB enforces ref types and
// cardinality, but a db/doc description does not enforce graph ownership.
fn validate_question_ownership(database: &Database) -> Result<usize> {
    let graph = PlacementGraph::read(database)?;
    let owner_attr = attribute(database, "question", "lesson")?;
    let primary_attr = attribute(database, "question", "primary-knowledge-point")?;
    let lesson_kps = attribute(database, "lesson", "knowledge-points")?;
    let kinds_attr = attribute(database, "entity", "kinds")?;
    let kp_kind = database
        .entid(&Keyword::new("kind", "knowledge-point"))
        .ok_or("missing KP kind")?;
    let mut owned = 0;
    for question in &graph.questions {
        let ancestors = graph.ancestors(*question);
        let ancestor_lessons: BTreeSet<_> =
            ancestors.intersection(&graph.lessons).copied().collect();
        // Standalone non-lesson questions need not invent a lesson owner.
        if ancestor_lessons.is_empty()
            && database.values(*question, owner_attr).is_empty()
            && database.values(*question, primary_attr).is_empty()
        {
            continue;
        }
        let owner = single_ref(database, *question, owner_attr, "owner lesson")?;
        let primary = single_ref(database, *question, primary_attr, "primary KP")?;
        require(
            graph.lessons.contains(&owner),
            "app/question-ownership: owner must be a lesson",
        )?;
        require(
            database
                .values(primary, kinds_attr)
                .contains(&&Value::Ref(kp_kind)),
            "app/question-ownership: primary skill must be a knowledge point",
        )?;
        require(
            database
                .values(owner, lesson_kps)
                .contains(&&Value::Ref(primary)),
            "app/question-primary-kp: primary KP must be taught by the owner lesson",
        )?;
        require(
            ancestor_lessons.iter().all(|lesson| *lesson == owner),
            "app/foreign-lesson-placement: question reaches a lesson other than its owner",
        )?;
        owned += 1;
    }
    Ok(owned)
}

fn expect_ownership_rejected(database: &Database, label: &str, transaction: &str) -> Result<()> {
    // Structural admission must succeed: the custom graph rule is checked here,
    // not incorrectly attributed to a native database constraint.
    let changed = database.with_edn(transaction, 11_000)?.db_after;
    match validate_question_ownership(&changed) {
        Err(error)
            if error
                .to_string()
                .starts_with("app/foreign-lesson-placement:") =>
        {
            println!("PASS application check rejects {label}");
            Ok(())
        }
        Err(error) => Err(format!("{label}: unexpected validation failure: {error}").into()),
        Ok(_) => Err(format!("{label}: invalid question ownership unexpectedly passed").into()),
    }
}

fn check_question_ownership(database: &Database) -> Result<()> {
    let owned = validate_question_ownership(database)?;
    require(
        owned == PlacementGraph::read(database)?.questions.len(),
        "fixture questions must all have lesson ownership and a primary KP",
    )?;
    println!("PASS application ownership and primary-KP coverage for {owned} fixture questions");
    let rows = query(
        database,
        "[:find ?q ?section :where [?q :entity/kinds :kind/question] [?p :placement/content ?q] [?p :placement/parent ?section] [?section :entity/kinds :kind/section]]",
    )?;
    require(
        !rows.is_empty(),
        "ownership regression requires a question inside a lesson section",
    )?;
    let question = entity_id(&rows[0][0])?;
    let section = entity_id(&rows[0][1])?;
    let owner_attr = attribute(database, "question", "lesson")?;
    let owner = single_ref(database, question, owner_attr, "owner lesson")?;
    let new_lesson = database.with_edn(
        r#"[{:db/id "ownership-test-lesson"
        :entity/id #uuid "00000000-0000-4000-8000-000000000001"
        :entity/kinds [:kind/lesson] :content/title "Ownership regression lesson"
        :db/ensure [:kind/lesson]}]"#,
        10_000,
    )?;
    let foreign = new_lesson.tempids["ownership-test-lesson"];
    let database = &new_lesson.db_after;
    expect_rejected(
        database,
        "multiple owner lessons",
        &format!(
            "[[:db/add {question} :question/lesson {owner}] [:db/add {question} :question/lesson {foreign}]]"
        ),
        "transaction/cardinality-one-conflict",
    )?;
    expect_rejected(
        database,
        "required lesson-question owner",
        &format!(
            "[[:db/retract {question} :question/lesson {owner}] [:db/ensure {question} :spec/lesson-question]]"
        ),
        "transaction/entity-spec",
    )?;
    for (label, child) in [
        ("direct placement in another lesson", question),
        ("sharing a question-bearing section across lessons", section),
    ] {
        expect_ownership_rejected(
            database,
            label,
            &format!(
                r#"[{{:db/id "foreign-placement"
            :entity/id #uuid "00000000-0000-4000-8000-000000000002"
            :entity/kinds [:kind/placement] :placement/parent {foreign}
            :placement/content {child} :placement/position 0 :db/ensure [:kind/placement]}}]"#
            ),
        )?;
    }
    Ok(())
}

fn check_assessment_fixture_novelty(database: &Database) -> Result<()> {
    let graph = PlacementGraph::read(database)?;
    let mut answered: BTreeMap<u64, BTreeSet<u64>> = BTreeMap::new();
    for row in query(
        database,
        r#"
        [:find ?learner ?question
         :where [?task :task/type :task.type/lesson]
                [?task :task/learner ?learner]
                [?attempt :attempt/task ?task]
                [?item :task-item/attempt ?attempt]
                [?item :task-item/outcome _]
                [?item :task-item/question ?question]]"#,
    )? {
        answered
            .entry(entity_id(&row[0])?)
            .or_default()
            .insert(entity_id(&row[1])?);
    }
    let assignments = query(
        database,
        "[:find ?learner ?assessment :where [?task :task/learner ?learner] [?task :task/assessment ?assessment]]",
    )?;
    let body = attribute(database, "content", "body")?;
    let mut comparisons = 0;
    for row in assignments {
        let learner = entity_id(&row[0])?;
        let assessment = entity_id(&row[1])?;
        let Some(lesson_questions) = answered.get(&learner) else {
            continue;
        };
        for question in &graph.questions {
            if !graph.ancestors(*question).contains(&assessment) {
                continue;
            }
            require(
                !lesson_questions.contains(question),
                "assessment fixture must not repeat a question ID this learner answered in a lesson",
            )?;
            let prompt = database.values(*question, body);
            require(!prompt.is_empty(), "assessment question must have a prompt")?;
            require(
                lesson_questions
                    .iter()
                    .all(|lesson_question| database.values(*lesson_question, body) != prompt),
                "assessment fixture must use different exact prompts from this learner's answered lesson questions",
            )?;
            comparisons += 1;
        }
    }
    require(
        comparisons > 0,
        "novelty fixture must contain a learner's answered lesson and assessment questions",
    )?;
    println!("PASS assessment fixture differs from this learner's answered lesson questions");
    Ok(())
}

// These checks read the illustrative state. They do not execute a scheduler,
// grader, XP calculator, or retention algorithm.
fn check_fixture_paths(database: &Database) -> Result<()> {
    expect_count(
        database,
        "manual lesson links to ordinary attempts, items, and part responses",
        r#"
        [:find ?task ?attempt ?item ?submission ?response
         :where [?task :task/origin :task.origin/learner]
                [?task :task/type :task.type/lesson]
                [?attempt :attempt/task ?task]
                [?item :task-item/attempt ?attempt]
                [?item :task-item/question ?question]
                [?question :question/parts ?part]
                [?submission :submission/task-item ?item]
                [?response :response/submission ?submission]
                [?response :response/part ?part]]"#,
        4,
    )?;
    expect_count(
        database,
        "two submissions remain distinct from one terminal item score",
        r#"
        [:find ?item ?first ?last
         :where [?item :task-item/score 1.0]
                [?first :submission/task-item ?item]
                [?first :submission/number 1]
                [?first :submission/final? false]
                [?first :submission/score 0.5]
                [?last :submission/task-item ?item]
                [?last :submission/number 2]
                [?last :submission/final? true]
                [?last :submission/score 1.0]]"#,
        1,
    )?;
    expect_count(
        database,
        "displayed B resolves to the accepted stable choice",
        r#"
        [:find ?item ?choice
         :where [?shown :presented-choice/label "B"]
                [?shown :presented-choice/position 1]
                [?shown :presented-choice/task-item ?item]
                [?shown :presented-choice/part ?part]
                [?shown :presented-choice/choice ?choice]
                [?choice :content/body "$4x^3$"]
                [?part :response-part/grading-rule ?rule]
                [?rule :grading-rule/accepted-choices ?choice]]"#,
        1,
    )?;
    expect_count(
        database,
        "manual learner has two concurrent enrollments",
        r#"
        [:find ?learner ?course
         :where [?task :task/origin :task.origin/learner]
                [?task :task/learner ?learner]
                [?enrollment :enrollment/learner ?learner]
                [?enrollment :enrollment/status :enrollment.status/active]
                [?enrollment :enrollment/course ?course]]"#,
        2,
    )?;
    expect_count(
        database,
        "manual lesson targets share global learner-skill state",
        r#"
        [:find ?learner ?skill ?progress
         :where [?task :task/origin :task.origin/learner]
                [?task :task/learner ?learner]
                [?task :task/targets ?skill]
                [?progress :progress/learner ?learner]
                [?progress :progress/skill ?skill]]"#,
        2,
    )?;
    expect_count(
        database,
        "stored XP award 12 is distinct from task nominal XP 10",
        r#"
        [:find ?task ?xp
         :where [?task :task/origin :task.origin/learner]
                [?task :task/nominal-xp 10]
                [?task :task/learner ?learner]
                [?attempt :attempt/task ?task]
                [?xp :xp-entry/attempt ?attempt]
                [?xp :xp-entry/learner ?learner]
                [?xp :xp-entry/amount 12]]"#,
        1,
    )?;
    expect_count(
        database,
        "fractional implicit credit links earned evidence to global progress",
        r#"
        [:find ?credit ?progress
         :where [?task :task/origin :task.origin/learner]
                [?task :task/learner ?learner]
                [?attempt :attempt/task ?task]
                [?item :task-item/attempt ?attempt]
                [?credit :credit/attempt ?attempt]
                [?credit :credit/task-item ?item]
                [?credit :credit/learner ?learner]
                [?credit :credit/kind :credit.kind/implicit]
                [?credit :credit/fraction 0.25]
                [?credit :credit/repetition-delta 0.25]
                [?credit :credit/skill ?skill]
                [?progress :progress/learner ?learner]
                [?progress :progress/skill ?skill]
                [?progress :progress/repetition 2.25]]"#,
        1,
    )?;
    expect_count(
        database,
        "unfinished recommended tasks have no earned credit in the fixture",
        r#"
        [:find ?credit
         :where [?task :task/origin :task.origin/recommended]
                [?attempt :attempt/task ?task]
                [?credit :credit/attempt ?attempt]]"#,
        0,
    )?;

    let blanks = query(
        database,
        "[:find ?q :where [?q :question/format :question.format/blank] [?item :task-item/question ?q] [?item :task-item/role :item.role/practice]]",
    )?;
    require(
        blanks.len() == 1,
        "expected one delivered practice blank question in the fixture",
    )?;
    let blank = entity_id(&blanks[0][0])?;
    let difficulty = attribute(database, "question", "difficulty-band")?;
    let gated = attribute(database, "question", "gated?")?;
    require(
        database.values(blank, difficulty).is_empty(),
        "unknown question difficulty must remain absent",
    )?;
    require(
        database.values(blank, gated).is_empty(),
        "unknown gate flag must remain absent",
    )?;
    let explicit_false = database
        .with_edn(
            &format!("[[:db/add {blank} :question/gated? false]]"),
            8_000,
        )?
        .db_after;
    require(
        explicit_false.values(blank, gated) == vec![&Value::Bool(false)],
        "explicit false must round-trip as a stored boolean",
    )?;
    require(
        database.values(blank, gated).is_empty(),
        "the captured database must retain the absent value",
    )?;
    println!("PASS unknown difficulty/gating remain absent and differ from explicit false");
    Ok(())
}

fn check_rejections(database: &Database) -> Result<()> {
    expect_rejected(
        database,
        "UUID type",
        r#"[{:db/id "bad-type" :entity/id "not-a-uuid"}]"#,
        "transaction/value-type",
    )?;
    let content = query(database, "[:find ?e :where [?e :content/body _]]")?;
    require(!content.is_empty(), "fixtures must contain a content body")?;
    let entity = entity_id(&content[0][0])?;
    expect_rejected(
        database,
        "cardinality one",
        &format!(
            r#"[[:db/add {entity} :content/body "conflict-a"] [:db/add {entity} :content/body "conflict-b"]]"#
        ),
        "transaction/cardinality-one-conflict",
    )?;
    let entities = query(database, "[:find ?e ?id :where [?e :entity/id ?id]]")?;
    let first = entity_id(&entities[0][0])?;
    let QueryValue::Scalar(second_uuid) = &entities[1][1] else {
        return Err("expected scalar UUID".into());
    };
    expect_rejected(
        database,
        "UUID uniqueness",
        &format!("[[:db/add {first} :entity/id {}]]", edn(second_uuid)?),
        "transaction/unique-conflict",
    )?;
    let questions = query(
        database,
        "[:find ?e :where [?e :entity/kinds :kind/question]]",
    )?;
    require(!questions.is_empty(), "fixtures must contain a question")?;
    let question = entity_id(&questions[0][0])?;
    let format_attribute = attribute(database, "question", "format")?;
    let formats = database.values(question, format_attribute);
    require(formats.len() == 1, "fixture question must have one format")?;
    expect_rejected(
        database,
        "required question format",
        &format!(
            "[[:db/retract {question} :question/format {}] [:db/ensure {question} :kind/question]]",
            edn(formats[0])?
        ),
        "transaction/entity-spec",
    )?;
    let progress = query(
        database,
        "[:find ?learner ?skill :where [?p :progress/learner ?learner] [?p :progress/skill ?skill]]",
    )?;
    require(
        !progress.is_empty(),
        "fixtures must contain global learner-skill progress",
    )?;
    expect_rejected(
        database,
        "duplicate global learner-skill state",
        &format!(
            r#"[{{:db/id "duplicate-progress" :progress/learner {} :progress/skill {}}}]"#,
            entity_id(&progress[0][0])?,
            entity_id(&progress[0][1])?,
        ),
        "transaction/unique-conflict",
    )?;
    Ok(())
}

fn run(directory: &Path) -> Result<()> {
    let mut database = Database::bootstrap()?;
    database = install(&database, &directory.join("01-attributes.edn"), 1_000)?;
    database = install(&database, &directory.join("02-entity-specs.edn"), 2_000)?;
    let mut examples: Vec<PathBuf> = std::fs::read_dir(directory.join("examples"))?
        .map(|entry| entry.map(|e| e.path()))
        .collect::<std::io::Result<_>>()?;
    examples.retain(|path| path.extension().is_some_and(|ext| ext == "edn"));
    examples.sort();
    require(
        examples.len() >= 2,
        "expected content and learning fixture transactions",
    )?;
    for (index, path) in examples.iter().enumerate() {
        database = install(&database, path, 3_000 + index as i64 * 1_000)?;
    }
    check_readback(&database)?;
    check_question_ownership(&database)?;
    check_assessment_fixture_novelty(&database)?;
    check_fixture_paths(&database)?;
    check_rejections(&database)?;
    println!("All schema smoke tests passed in memory; no durable database was opened.");
    Ok(())
}

fn main() {
    let directory = std::env::args_os()
        .nth(1)
        .map(PathBuf::from)
        .unwrap_or_else(|| PathBuf::from("schema"));
    if let Err(error) = run(&directory) {
        eprintln!("FAIL {error}");
        std::process::exit(1);
    }
}
