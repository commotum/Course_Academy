class TaskEventStorage {
    static init(taskId) {
        this.taskId = taskId;
        this.events = this.getStoredEvents(this.taskId);
    }

    static storeEvent(event) {
        this.events.push(event);

        const key = this.getKey();
        const str = JSON.stringify(this.events);

        localStorage.setItem(key, str);
    }

    static storeEvents(events) {
        this.events = events.slice(); // Copy array elements

        const key = this.getKey();
        const str = JSON.stringify(this.events);

        localStorage.setItem(key, str);
    }
    
    static getStoredEvents() {
        const key = this.getKey();
        const str = localStorage.getItem(key);
        const events = str ? JSON.parse(str) : [];

        for(let event of events) {
            event.localTimestamp = new Date(event.localTimestamp);
        }

        return events;
    }

    static removeStoredEvents(taskId) {
        this.events = [];

        const key = this.getKey(taskId);
        localStorage.removeItem(key);
    }

    static getKey(taskId) {
        taskId = taskId ? taskId : this.taskId;
        return 'task-' + this.taskId + '-events';
    }    

    static isLocalStorageAvailable() {
        const test = 'test';

        try {
            localStorage.setItem(test, test);
            localStorage.removeItem(test);
            return true;
        } catch(e) {
            return false;
        }
    }
}