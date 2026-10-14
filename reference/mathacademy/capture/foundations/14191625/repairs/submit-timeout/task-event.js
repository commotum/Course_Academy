class TaskEvent {
    static init(taskId) {
        this.taskId = taskId;
        this.prevEvent = null;
        this.visible = false;
        this.resendAttempt = 0;

        TaskEventStorage.init(taskId);
        this.postStoredEvents();                

        this.post('window', 'onLoad');

        this.updateVisibility(true);

        window.addEventListener('beforeunload', () => { this.post('window', 'onUnload'); });
        window.addEventListener('focus', () => { this.post('window', 'onFocus'); });
        window.addEventListener('blur', () => { this.post('window', 'onBlur'); });
        window.addEventListener('copy', () => { this.post('window', 'onCopy'); });        
        window.addEventListener('paste', () => { this.post('window', 'onPaste'); });                

        setInterval(() => {
            let visible = !(document.hidden || document.msHidden || document.webkitHidden || document.mozHidden);
            this.updateVisibility(visible);        
        }, 1000);
    }

    static updateVisibility(visible) {
        if (visible === this.visible) { return; }
        this.visible = visible;
        const type = this.visible ? 'onVisible' : 'onHidden';
        this.post('window', type);    
    }

    static postSync(source, type, sourceId) {
        return new Promise((resolve, reject) => {
            this.post(source, type, sourceId, (response) => {
                if (response.error) {
                    resolve(response.error);
                } else {
                    resolve(null);
                }
            });
        });
    }

    static post(source, type, sourceId, callback) {
        let event = { taskId: this.taskId, source, type, sourceId };

        if (!this.equal(event)) {
            this._postEvent(event, callback);            
        } else {
            if (callback) {
                callback(null);
            }
        }
    }

    static postDelay(source, type, sourceId, callback) {
        let event = { taskId: this.taskId, source, type, sourceId };

        if (this.equal(event, this.prevEvent)) {
            clearTimeout(this.timer);
            this.timer = null;
        } 

        this.timer = setTimeout(evt => {
            this._postEvent(event, callback);
            this.timer = null;
        }, 1000);
    }

    static async _postEvent(event, callback) {  
        event.localTimestamp = new Date();
        event.sendAttempt = 1;

        this.prevEvent = event;        

        if (TaskEventStorage.events.length > 0) {
            // We're already waiting to make another attempt, so just store the event in the buffer
            TaskEventStorage.storeEvent(event);

            if (callback) {
                callback();
            } 
        } else {
            const response = await APISync.postTaskEvents(this.taskId, event);
        
            if (!response) {
                TaskEventStorage.storeEvent(event);
                this.storeNetworkErrorEvent();
                this.tryAgainLater();
            }            

            if (callback) {
                callback(response);
            }  
        }                  
    }

    static storeNetworkErrorEvent() {
        TaskEventStorage.storeEvent({ 
            localTimestamp: new Date(),
            sendAttempt: 1,
            taskId: this.taskId, 
            source: 'window', 
            type: 'onNetworkError' 
        });
    }

    static tryAgainLater() {
        const timeoutMS = this.getTimeoutMS();
        setTimeout(this.postStoredEvents.bind(this), timeoutMS);        
    }

    static async postStoredEvents() {        
        const events = TaskEventStorage.events;

        if (!events.length) { return; }

        TaskEventStorage.removeStoredEvents();

        for(const event of events) {
            event.sendAttempt++;
        }

        const response = await APISync.postTaskEvents(this.taskId, events);
        
        if (!response) {
            TaskEventStorage.storeEvents(events);
            this.storeNetworkErrorEvent();
            this.tryAgainLater();
        }
    }

    static getTimeoutMS() {
        const TIMEOUTS = [ 5, 10, 15, 20, 30, 45, 60 ]; // Seconds

        this.resendAttempt++;
        this.resendAttempt = Math.min(this.resendAttempt, TIMEOUTS.length);

        const timeout = TIMEOUTS[this.resendAttempt - 1];

        return timeout * 1000;
    }

    static equal(a, b) {
        if (!a || !b) { return false; }

        if (a.taskId !== b.taskId) { return false; } 
        if (a.source !== b.source) { return false; }             
        if (a.type !== b.type) { return false; }    
        if (a.sourceId !== b.sourceId) { return false; }

        return true;
    }
}