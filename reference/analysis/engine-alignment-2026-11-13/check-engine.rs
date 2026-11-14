use course_academy_engine::activities::{evaluate_kp_prefix,evaluate_review_prefix,earned_xp};
fn main(){
 for s in ["WWCC","WWCCC","WWCCW","WCWCW","CCWCW"] {
 let xs:Vec<_>=s.chars().map(|c|Some(c=='C')).collect();
 println!("{s} lesson={:?} review={:?}",evaluate_kp_prefix(&xs),evaluate_review_prefix(&xs));
 }
 println!("lesson XP base18 correct8 total11 = {:?}",earned_xp("lesson",18i64,8,11,Some(false)));
}