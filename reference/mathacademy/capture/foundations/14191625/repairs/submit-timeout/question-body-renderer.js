class QuestionBodyRenderer {
    async render(container, questionId, segments, locked) {
        this.container = container;
        this.questionId = questionId;
        this.segments = segments;
        this.locked = locked;
        this.selectLists = [];

        await this.renderSelectLists(segments);

        //this.container.innerHTML = this.stripEnclosingParagraphTags(this.container.innerHTML);

        this.constructHTML();
        //this.container.innerHTML += mathdown.process(this.html);
        this.container.innerHTML += this.html;

        CodeRenderer.highlight(this.container);  

        this.insertCodeSelectSpanPlaceholders();

        await renderLatex([this.container]);

        this.insertSelectLists();    

        return this.selectLists;
    }

    constructHTML() {
        this.html = '';
        this.insideSection = false;
        this.selectIndex = 0;

        if (this.hasMultipleSections()) {
            this.html += '<span class="proofSection">';
            this.insideSection = true;
        }
        
        for(const segment of this.segments) {
            const segmentHTML =  this.processSegement(segment);
            this.html += segmentHTML;
        }

        if (this.insideSection) {
            this.html += '</span>';
        }    

        this.html = CodeRenderer.process(this.html);
    }

    hasMultipleSections() {
        for(const segment of this.segments) {
            if (segment.sectionDivider) { 
                return true; 
            }
        }
        return false;
    }

    processSegement(segment) {
        if (segment.sectionDivider) { 
            return this.processSectionSegment(); 
        } else if (segment.newParagraph) { 
            return this.processParagraphSegement(segment.newParagraph); 
        } else if (segment.text) { 
            return this.processTextSegment(segment.text); 
        } else if (segment.code) { 
            return segment.code; 
        } else if (segment.mathJax) { 
            return segment.mathJax; 
        } else if (segment.select) { 
            return this.processSelectSegment(segment.select); 
        } else { 
            return ''; 
        }
    }

    processSectionSegment() {
        return this.insideSection ? '</span><span class="proofSection">' : '<span class="proofSection">';
    }

    processParagraphSegement() {
        return '<p></p>';
    }

    processTextSegment(text) {
        // processBasic instead of process: text segments are inline (interleaved with LaTeX and
        // selects), so we must not introduce <p> tags that process/marked would add.
        const textWithMarkdown = mathdown.processBasic(text);
        return CodeRenderer.process(textWithMarkdown);
    }

    processSelectSegment(select) {
        const selectList = this.selectLists[this.selectIndex];
        const placeholderHTML = selectList.getPlaceholder();

        this.selectIndex++;

        if (select.context === 'mathJax') {                    
            return placeholderHTML;
        } else if (select.context === 'code') {                    
            return `__${placeholderHTML}__`;                    
        } else {
            return `<span class="selectListPlaceholder">${placeholderHTML}</span>`;
        }        
    }

    removeParagraphTags(str) {
        return str.replace(/<p[^>]*>|<\/p>/g, '');
    }    

    insertCodeSelectSpanPlaceholders() {
        for(let i = 0; i < this.selectLists.length; i++) {
            const html = this.container.innerHTML;
            const selectId = 'S' + i;
            const placeholder = `__S${i}__`;
            const spanPlaceholderHTML = `<span id="${selectId}" class="selectListPlaceholder">${selectId}</span>`;
            this.container.innerHTML = html.replace(placeholder, spanPlaceholderHTML);
        }
    }

    async renderSelectLists(segments) {
        let renderFarm = this.getRenderFarm();

        for(let segment of segments) {
            if (segment.select) {
                let selectList = new SelectList(renderFarm, this.container.id, this.questionId, segment.select);   
                selectList.sectionIndex = segment.select.sectionIndex;                        
                this.selectLists.push(selectList);

                if (this.locked) {
                    selectList.locked = true;
                }
            }
        }

        await renderLatex([renderFarm]);

        this.resizeSelectLists();        
    }

    insertSelectLists() {
        this.insertTextNodeSelectLists();
        this.insertSpanSelectLists();
    }

    insertTextNodeSelectLists() {
        let inserted = {};

        let textNodePlaceholders = this.findTextNodeSelectPlaceholders();
        for(let textNodePlaceholder of textNodePlaceholders) {
            let text = this.getTextNodeAsString(textNodePlaceholder);

            if (text === '()') {
                text = this.getTextNodeAsStringFirefox(textNodePlaceholder);
            }

            let selectId = text.substring(1, text.length - 1);

            if (inserted[selectId]) { continue; }

            inserted[selectId] = 1;

            let selectList = this.getSelectListById(selectId);

            if (selectList) {
                this.fixListMathjax(selectList.element);

                let scriptNode = textNodePlaceholder.parentNode;
                let msubNode = scriptNode.parentNode;
                let mrowNode = msubNode.parentNode;

                mrowNode.innerHTML = '';
                mrowNode.appendChild(selectList.element);

                selectList.init();
            }
        }
    }

    insertSpanSelectLists() {
        let spanPlaceholders = this.findSpanSelectPlaceholders();
        for(let spanPlaceholder of spanPlaceholders) {
            let selectId = spanPlaceholder.innerHTML;
            let selectList = this.getSelectListById(selectId);

            if (selectList) {
                spanPlaceholder.replaceWith(selectList.element);

                selectList.init();
            }
        }
    }

    getSelectListById(selectId) {
        for(let selectList of this.selectLists) {
            if (selectList.id === selectId) {
                return selectList;
            }
        }
        return null;
    }

    resizeSelectLists() {
        for(let selectList of this.selectLists) {
            selectList.resize();
        }          
    }
    
    findTextNodeSelectPlaceholders() {
        let placeholders = [];

        let nodes = this.container.querySelectorAll('mjx-texatom');
        for(let node of nodes) {
            if (this.isAssistiveDecendant(node)) { continue; } 
            if (!this.isMathjaxSelectPlaceholder(node) && !this.isMathjaxSelectPlaceholderFirefox(node)) {
                continue;
            }

            placeholders.push(node);            
        }

        return placeholders;
    }

    findSpanSelectPlaceholders() {
        return this.container.querySelectorAll('.selectListPlaceholder');
    }

    isAssistiveDecendant(node) {
        let n = node.parentNode;
        while (n && n !== this.container) {
            if (n.nodeName === 'MJX-ASSISTIVE-MML') {
                return true;
            }

            n = n.parentNode;
        }
        return false;
    }

    isMathjaxSelectPlaceholder(textNode) {
        if (textNode.childNodes.length < 4) { return false; }

        let text = this.getTextNodeAsString(textNode);
        if (!text || text.length < 3) { return false; }

        let prefix = text.substring(0, 2).toUpperCase();

        if (prefix !== '(S') {
            return false;
        }
        return true;
    }

    getTextNodeAsString(textNode) {
        let str = '';
        for(let i = 0; i < textNode.childNodes.length; i++) {
            let childNode = textNode.childNodes[i];

            for (let charNode of childNode.childNodes) {
                let className = charNode.classList[0];
                if (!className) { continue; }
    
                let parts = className.split('-');
                let charCode = parts[1].substring(1);
    
                let char;
                
                if (charCode.length === 5 && charCode === '1D446') { 
                    // 1D446 is unicode for the letter 'S'
                    char = 'S'
                } else {
                    char = this.hex2a(charCode);
                } 
    
                str += char;
            }
        }

        return str;
    }

    isMathjaxSelectPlaceholderFirefox(textNode) {
        if (textNode.childNodes.length < 3) { return false; }

        let text = this.getTextNodeAsStringFirefox(textNode);
        if (!text || text.length < 3) { return false; }

        let prefix = text.substring(0, 2).toUpperCase();

        if (prefix !== '(S') {
            return false;
        }
        return true;
    }

    getTextNodeAsStringFirefox(textNode) {
        let str = '';
        for(let i = 0; i < textNode.childNodes.length; i++) {
            let childNode = textNode.childNodes[i];

            for (let charNode of childNode.childNodes) {
                let className = charNode.classList[0];
                if (!className) { continue; }
    
                let parts = className.split('-');
                let charCode = parts[1].substring(1);

                if (charCode === "") {
                    let grandchildNode = charNode.childNodes[0];

                    className = grandchildNode.classList[0];
                    if (!className) { continue; }

                    parts = className.split('-');
					charCode = parts[1].substring(1);
                }
    
                let char;
                
                if (charCode.length === 5 && charCode === '1D446') { 
                    // 1D446 is unicode for the letter 'S'
                    char = 'S'
                } else {
                    char = this.hex2a(charCode);
                } 

                if (char === ' b') { continue; }
    
                str += char;
            }
        }

        return str;
    }
    
    hex2a(hexx) {
        let hex = hexx.toString();
        let str = '';
        for (let i = 0; i < hex.length; i += 2) {
            str += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
        }

        return str;
    }

    findParentWithClass(element, className) {
        let node = element;
        while (!node.classList.contains(className)) {
            node = node.parentNode;
        }
        return node;
    }

    updateControllingHeight(selectList) {
        let node = selectList.parentNode;
        while (node) {
            if (!node || !node.style) { break; }

            if (node.style.height) {
                node.style.height = 'fit-content';
                break;
            }
            node = node.parentNode;
        }
    }

    fixListMathjax(selectList) {
        let optionDivs = selectList.querySelectorAll('.selectListOption');

        for(let optionDiv of optionDivs) {
            let mjxContainer = optionDiv.querySelector('mjx-container');
            if (mjxContainer) {
                mjxContainer.style.fontSize = '100%';
            }

            let mjxMath = optionDiv.querySelector('mjx-math');
            if (mjxMath) {

                let isFirefox = typeof InstallTrigger !== 'undefined';

                if (isFirefox) {
                    mjxMath.style.paddingTop = '3px';
                } else {
                    mjxMath.style.paddingTop = '2px';
                }
            }
        }
    }

    getRenderFarm() {
        let renderFarm = document.getElementById('renderFarm');
        if (!renderFarm) {
            renderFarm = document.createElement('div');
            renderFarm.id = 'renderFarm';
            renderFarm.style.position = 'absolute';
            renderFarm.style.left = '-10000px';
            renderFarm.style.visibility = 'hidden';
            document.body.appendChild(renderFarm);
        }        

        return renderFarm;
    }

    removeHelpeScriptsFromOptions(selectList) {
        let scripts = selectList.querySelectorAll('script');
        for(let script of scripts) {
            script.parentNode.removeChild(script);
        }
    }

    // This function adds 4 pixels to the bottom margin of selects of it's on a Mac, the selects 
    // are in MathJax blocks and they're NOT in the numerator of a fraction. 
    adjustSelectMargins(segments) {
        let isMacOS = navigator.platform.toUpperCase().indexOf('MAC') >= 0;

        if (isMacOS) {
            let insideMathJaxBlock = false;

            for(let i = 0; i < segments.length; i++) {
                let segment = segments[i];

                if (segment.mathJax) {
                    if (!insideMathJaxBlock) {
                        insideMathJaxBlock = this.isOpeningMathJaxBlock(segment.mathJax);
                    } else {
                        if (this.isClosingMathJaxBlock(segment.mathJax)) {
                            insideMathJaxBlock = false;
                        }
                    }
                } else if (segment.select) {
                    segment.select.insideMathJaxBlock = insideMathJaxBlock;
                      
                    if (insideMathJaxBlock) {
                        let prevSegment = segments[i - 1];

                        if (prevSegment.mathJax) {
                            segment.select.insideDfrac = this.isOpeningDfrac(prevSegment.mathJax);

                            if (!segment.select.insideDfrac) {
                                segment.select.margin.bottom += 4;
                            }
                        }
                    }
                } 
            }
        }
    }
}