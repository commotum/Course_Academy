// Requires: SegmentParser, BlockParser, GraphicsParser, QuestionBodySection, Select, Textbox

class QuestionBody {
    constructor(source, graphics) {
        this.source = GraphicsParser.insertGraphics(source, graphics); 

        this.segments = [];
        this.inputs = [];
        this.inputsById = {};

        this.parseBlocks();
        this.parseInputs();
        this.parseSectionDividers();
        this.parseParagraphs();

        //this.processLineBreaks();        

        this.discardUnusedSegments();
        this.createSections();
    }

    parseBlocks() {
        this.blocks = BlockParser.parse(this.source);
    }
    
    parseInputs() {
        this.segments = [];
        for(const block of this.blocks) {
            const segments = this.parseBlockInputs(block);
            this.segments = this.segments.concat(segments);
        }    
    }

    parseBlockInputs(block) {
        const DELIMITERS = [ 
            { type: 'select', open: 'SELECT[', close: ']' }, 
            { type: 'textbox', open: 'TEXTBOX[', close: ']' } 
        ];

        const controlChars = this.getControlChars(block.type);

        let blockText;

        if (block.type === 'code') {
            blockText = this.stipCodeBlockDelimiters(block.text);
        } else {
            blockText = block.text;
        }

        const results = SegmentParser.parse(blockText, DELIMITERS, controlChars);  

        const segments = [];
        for(const result of results) {
            const segment = {};

            if (result.matched) {
                segment.input = this.createInput(result, block.type);
            } else {
                segment[block.type] = result.content;
            }

            segments.push(segment);
        }

        // Add back code-block delimiters
        if (block.type === 'code') {
            segments[0].code = '```' + segments[0].code;
            segments[segments.length - 1].code += '```';
        }

        return segments;
    }

    stipCodeBlockDelimiters(src) {
        return src.substring(3, src.length - 3);        
    }

    getControlChars(blockType) {
        switch (blockType) {
            case 'code': return ['`', '"'];
            case 'mathJax': return ['"'];
            default: return ['$', '`', '"'];
        }
    }

    createInput(result, context) {
        const type = result.delimiters.type;
        const source = result.inner;
        const index = this.inputs.length;

        let input;

        switch (type) {
            case 'textbox': input = new Textbox(source, index); break;
            case 'select': input = new Select(source, index); break;
        }

        input.context = context;

        if (type === type && context === 'code') {
            this.stripBackTicksFromSelectOptions(input);
        }
        
        this.inputs.push(input)

        if (input.id) {
            this.inputsById[input.id] = input;
        }

        return input;
    }

    stripBackTicksFromSelectOptions(select) {
        for(let i = 0; i < select.options.length; i++) {
            let option = select.options[i];

            if (option[0] === '`' && option[option.length - 1] === '`') {
                option = option.substring(1, option.length - 1);
                select.options[i] = option;
            }
        }
    }

    parseSectionDividers() {
        let segments = [];

        for(const segment of this.segments) {
            if (segment.text) {
                const newSegments = this.parseSegmentSectionDividers(segment);
                segments = segments.concat(newSegments);
            } else {
                segments.push(segment);
            }
        }

        this.segments = segments;
    }

    parseSegmentSectionDividers(segment) {
        const newSegments = [];
        const parts = segment.text.split('|||');

        for(let i = 0; i < parts.length; i++) {
            const part = parts[i];

            newSegments.push({ text: part });

            if (i < (parts.length - 1)) {
                newSegments.push({
                    sectionDivider: true
                });
            }
        }

        return newSegments;
    }

    parseParagraphs() {
        let segments = [];

        for(const segment of this.segments) {
            if (segment.text) {
                const newSegments = this.parseSegmentParagraphs(segment);
                segments = segments.concat(newSegments);
            } else {
                segments.push(segment);
            }
        }

        this.segments = segments;
    }

    parseSegmentParagraphs(segment) {
        const newSegments = [];
        const parts = segment.text.split('\n\n');

        for(let i = 0; i < parts.length; i++) {
            const part = parts[i];

            newSegments.push({ text: part });

            if (i < (parts.length - 1)) {
                newSegments.push({ newParagraph: true });
            }
        }

        return newSegments;
    }

    discardUnusedSegments() {
        for(let i = (this.segments.length - 1); i >= 0; i--) {
            const prevSegment = i > 0 ? this.segments[i - 1] : null;
            const segment = this.segments[i];

            if (segment.hasOwnProperty('text') && segment.text.trim() == '') {
                this.segments.splice(i, 1);
            } else if (prevSegment && prevSegment.newParagraph && segment.newParagraph) {
                this.segments.splice(i, 1);
            } else if (prevSegment && prevSegment.newParagraph && segment.sectionDivider) {
                this.segments.splice(i - 1, 1);
            }
        }
    }

    createSections() {
        this.sections = [];

        let segments = [];
        for(const segment of this.segments) {
            if (segment.sectionDivider) {
                this.createSection(segments);
                segments = [];
            }
            segments.push(segment);
        }
        this.createSection(segments);
    }

    createSection(segments) {
        if (segments.length > 0) {
            const index = this.sections.length;
            const section = new QuestionBodySection(index, segments);
            this.sections.push(section);
        }
    }
    
    isComplete() {
        for(const section of this.sections) {
            if (!section.complete) { 
                return false;
            }
        }        
        return true;       
    }

    getVisibleSegments() {
        const segments = [];     

        let prevSection;
        for(const section of this.sections) {
            if (!prevSection || prevSection.complete) {
                for(const segment of section.segments) {
                    segments.push(segment);
                }
            }
            prevSection = section;
        }       

        return segments;
    }
}
