// Requires Splitter

class Input { 
    constructor(source, index) {
        this.source = source;
        this.index = index;

        this.margin = { left: 0, right: 0, top: 0, bottom: 0 };
    }

    isValid() {
        return this.index >= 0;
    }

    parse() {
        const parts = Splitter.split(this.source, ';', ['$', '`', '"']);    

        for(let i = 0; i < parts.length; i++) {
            const part = parts[i];
            const section = this.createSection(i, part);

            this.parseSections(section);
        }
    }

    // Virtual method
    parseSection(section) {}
    
    createSection(index, source) {
        const section = {
            index,
            name: null,
            data: null
        };   

        const parts = Splitter.split(source, ':', ['$', '`', '"']); 

        if (parts.length === 1) {    
            section.data = parts[0].trim();
        } else if (parts.length === 2) {
            section.name = parts[0].trim().toLowerCase();
            section.data = parts[1].trim();
        }

        return section;
    }

    parseSections(section) {
        switch (section.name) {
            case 'margins': this.parseMargins(section.data); break;                        
            case 'margin-left': this.parseMarginLeft(section.data); break;
            case 'margin-right': this.parseMarginRight(section.data); break;
            case 'margin-top': this.parseMarginTop(section.data); break;         
            case 'margin-bottom': this.parseMarginBottom(section.data); break;   
            default: this.parseSection(section); break;
        }
    }

    parseMargins(src) {
        const margins = src.split(',');

        if (margins.length === 4) {
            this.margin.top = this.parseInt(margins[0]);
            this.margin.right = this.parseInt(margins[1]);
            this.margin.bottom = this.parseInt(margins[2]);
            this.margin.left = this.parseInt(margins[3]);
        }        
    }

    parseMarginLeft(src) {
        this.margin.left = this.parseInt(src);        
    }
    parseMarginRight(src) {
        this.margin.right = this.parseInt(src);        
    }
    parseMarginTop(src) {
        this.margin.top = this.parseInt(src);        
    }
    parseMarginBottom(src) {
        this.margin.bottom = this.parseInt(src);        
    }

    stripDoubleQuotes(option) {
        option = option.trim();

        const firstChar = option[0];
        const lastChar = option[option.length-1];

        if (firstChar === '"' && firstChar === lastChar) {
            return option.slice(1, option.length-1);
        } else {
            return option;
        }
    }

    parseInt(str) {
        return this.isInteger(str) ? parseInt(str) : 0;
    }

    isInteger(str) {
        return !isNaN(str) && Number.isInteger(parseFloat(str));
    }
}
