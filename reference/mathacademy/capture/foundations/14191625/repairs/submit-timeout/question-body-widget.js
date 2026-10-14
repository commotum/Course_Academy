var _nextSelectIndex = 1;

class QuestionBodyWidget {
    constructor(container) {
        this.container = container;
        this.selects = [];   
    }

    onSelect(questionBody, select) {}

    async init(questionId, source, locked = false) {
        this.questionId = questionId;
        this.locked = locked;
    

        if (Array.isArray(source)) {
            this.segments = source;
        } else {
            const body = new QuestionBody(source);
            this.segments = body.segments;
        }

        this.convertInputsToSelects();

        this.setSectionIndexes(this.segments);

        this.container.innerHTML = this.stripEnclosingParagraphTags(this.container.innerHTML);

        let renderer = new QuestionBodyRenderer();
        let selects = await renderer.render(this.container, questionId, this.segments, locked);

        for(let select of selects) {
            select.onSelect = (select) => {
                this.onSelect(this, select);
            };
            this.selects.push(select);
        }
    }

    convertInputsToSelects() {
        // TEMPORARY: Convert segment.input to expected segment.select object
        for(const segment of this.segments) {
            if (segment.input) {
                segment.select = segment.input;
                delete segment.input;;
            }
        }     
    }

    async update(segments) {
        this.setSectionIndexes(segments);

        let renderer = new QuestionBodyRenderer();
        let selects = await renderer.render(this.container, this.questionId, segments);

        for(let select of selects) {
            select.onSelect = (select) => {
                this.onSelect(this, select);
            };
            this.selects.push(select);
        }
    }

    setSectionIndexes(segments) {
        let sectionIndex = 0;
        for(let segment of segments) {
            if (segment.sectionDivider) {
                sectionIndex++;
            }

            if (segment.select) {
                segment.select.sectionIndex = sectionIndex;
            }
        }
    }

    enable() {
        for(let select of this.selects) {
            select.enable();
        }
    }

    disable() {
        for(let select of this.selects) {
            select.disable();
        }
    }

    getSelectListById(selectId) {
        for(let select of this.selects) {
            if (select.id === selectId) {
                return select;
            }
        }
        return null;
    }

    stripEnclosingParagraphTags(str) {
        if (str && str.length > 0) {
            str = str.trim();

            let start = str.substring(0, 3);
            let end = str.substring(str.length - 4);

            if (start === '<p>' && end === '</p>') {
                str = str.substring(3, str.length - 4);
            } 
        }

        return str;
    }

    markCorrect(select) {
        select.setCorrect();

        if (select.proofSection) {
            if (this.isSectionComplete(select.proofSection)) {
                this.showNextSection();
            }
        }
    }

    markIncorrect(select) {
        select.setIncorrect();
    }

    getAnswers(includeIds) {
        let answers = [];
        for(let select of this.selects) {
            let selectedIndex = select.getSelectedIndex();

            if (selectedIndex !== -1) {

                if (includeIds) {
                    answers.push({
                        selectId: select.config.id,
                        selectIndex: select.config.index,
                        selectedIndex
                    });
                } else {
                    answers.push(selectedIndex);
                }
            }
        }

        return answers;
    }

    isSectionComplete(proofSection) {
        for(let select of proofSection.selects) {
            if (!select.correct) {
                return false;
            }
        }
        return true;
    }

    reset() {
        let proofSections = this.container.querySelectorAll('.proofSection');

        if (proofSections.length === 0) { return; }

        proofSections[0].style.visibility = 'visible';

        for(let i = 1; i < proofSections.length; i++) {
            proofSections[i].style.visibility = 'hidden';
        }

        for(let select of this.selects) {
            select.reset();
        }   
    }

    showAll() {        
        let proofSections = this.container.querySelectorAll('.proofSection');

        for(let proofSection of proofSections) {
            proofSection.style.visibility = 'visible';
        }
    }

    showNextSection() {        
        let proofSections = this.container.querySelectorAll('.proofSection');

        for(let proofSection of proofSections) {
            if (proofSection.style.visibility === 'hidden') {
                proofSection.style.visibility = 'visible';
                break;
            }
        }
    }

    renderCorrectProof() {
        let arr = [];
        for(let segment of this.segments) {
            if (segment.text) {
                arr.push(segment.text);
            } else if (segment.mathJax) {
                arr.push(segment.mathJax);
            } else if (segment.select) {
                if (segment.select.options.length > 0) {
                    let correctOption = segment.select.options[0];
                    arr.push(correctOption);
                }
            } else if (segment.newParagraph) {
                arr.push('<p>');
            }
        }

        let text = '\n\nThe full proof is provided below.\n\n>' + arr.join('');

        return text;        
    }
}