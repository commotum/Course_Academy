var API = {   

    getNotificationPreferences: function(userKey, callback) {
        this._get('/api/users/' + userKey + '/notification-preferences', callback); 
    },

    updateNotificationPreferences: function(userKey, data, callback) {
        this._post('/api/users/' + userKey + '/notification-preferences', data, callback);
    },    

    unsubscribeFromProductAnnouncements: function(userKey, callback) {
        const data = {};

        this._post('/api/unsubscribe/product-announcements?key=' + userKey, data, callback);
    },

    updateTimeZone: function(timeZone, callback) {
        const data = { timeZone };
        this._post('/api/users/time-zone', data, callback);
    },

    createAccountTransferRequest: function(data, callback) {
        this._post('/api/account-transfer', data, callback);
    },

    searchGraphics: function(searchText, topicId, callback) {
        const encodeSearchText = encodeURIComponent(searchText);

        let query = `search=${encodeSearchText}`;

        if (topicId) {
            query += `&topicId=${topicId}`;
        }

        this._get('/api/search/graphics?' + query, callback);
    },
    
    searchExamples: function(searchText, formats, offset, callback) {
        const encodeSearchText = encodeURIComponent(searchText);
        this._get('/api/search/examples?search=' + encodeSearchText + '&formats=' + formats.join(',') + '&offset=' + offset, callback);
    },

    getExemplars: function(exampleId, formats, callback) {
        this._get('/api/examples/' + exampleId + '/exemplars?formats=' + formats.join(','), callback);
    },

    getExampleGraphics: function(topicId, exampleId, callback) {
        this._get('/api/topics/' + topicId + '/graphics?exampleId=' + exampleId, callback);
    },

    getTutorialGraphics: function(topicId, tutorialId, callback) {
        this._get('/api/topics/' + topicId + '/graphics?tutorialId=' + tutorialId, callback);
    },

    reportError: function(data, callback) {
        this._post('/api/client-errors', data, callback);
    },

    updateUserCategories(userId, categories, callback) {
        const data = { userId, categories };
        this._post('/api/users/' + userId + '/categories', data, callback);
    },

    createCharterStudentAccount(data, callback) {
        this._post('/api/students/create-charter-account', data, callback);
    },

    updateCharterStudentAccount(studentId, data, callback) {
        this._post('/api/students/' + studentId + '/update-charter-account', data, callback);
    },      

    transferCharterStudentAccount(studentId, data, callback) {
        this._post('/api/students/' + studentId + '/transfer-charter-account', data, callback);
    },      

    generateUserPassword(userId, callback) {
        const data = { userId };
        this._post('/api/users/' + userId + '/generate-password', data, callback);
    },

    cancelStudentAccount(studentId, cancelSubscription, refund, cancelReason, deactivateImmediately, callback) {
        const data = { studentId, cancelSubscription, refund, cancelReason, deactivateImmediately };
        this._post('/api/students/' + studentId + '/cancel', data, callback);
    },

    deactivateAccount(studentId, callback) {
        this._post('/api/students/' + studentId + '/deactivate', { studentId }, callback);
    },

    getSchool(schoolId, callback) {
        this._get('/api/schools/' + schoolId, callback);
    },    

    searchSchools(lookup, callback) {
        this._post('/api/schools/search', { lookup }, callback);
    }, 

    getSchoolInstructors(callback) {
        this._get('/api/instructors', callback);
    },

    getUserSchool(callback) {
        this._get('/api/school', callback);
    },

    getSchoolClasses(callback) {
        this._get('/api/classes', callback);
    },

    getClass(classId, callback) {
        this._get('/api/classes/' + classId, callback);
    },    

    moveStudentToClass(studentId, classId, callback) {
        this._post('/api/students/' + studentId + '/move-to-class', { studentId, classId }, callback);
    },

    createSchool(data, callback) {
        this._post('/api/schools/create', data, callback);
    },

    updateSchool(schoolId, data, callback) {
        this._post('/api/schools/' + schoolId + '/update', data, callback);
    },

    createOrganization(data, callback) {
        this._post('/api/organizations/create', data, callback);
    },

    getStripeProducts(callback) {
        this._get('/api/stripe/products', callback);
    },

    updateOrganization(organizationId, data, callback) {
        this._post('/api/organizations/' + organizationId + '/update', data, callback);
    },

    getOrganization(organizationId, callback) {
        this._get('/api/organizations/' + organizationId, callback);
    },

    getOrganizations(callback) {
        this._get('/api/organizations', callback);
    },

    getOrganizationSchools(organizationId, callback) {
        this._get('/api/organizations/' + organizationId + '/schools', callback);
    },

    activateOrganizationAccount(organizationId, data, callback) {
        this._post('/api/organizations/' + organizationId + '/activate', data, callback);
    },

    cancelOrganizationAccount(organizationId, callback) {
        const data = { organizationId };

        this._post('/api/organizations/' + organizationId + '/cancel', data, callback);
    },

    searchOrganizations(lookup, callback) {
        this._post('/api/organizations/search', { lookup }, callback);
    },

    importStudents(schoolId, data, callback) {
        this._post('/api/schools/' + schoolId + '/import-students', data, callback);
    },

    cancelSchoolAccount(schoolId, callback) {
        const data = { schoolId };

        this._post('/api/schools/' + schoolId + '/cancel', data, callback);
    },

    reactivateSchoolAccount(schoolId, callback) {
        const data = { schoolId };

        this._post('/api/schools/' + schoolId + '/reactivate', data, callback);
    },

    createClass(data, callback) {
        this._post('/api/classes/create', data, callback);
    },

    updateClass(classId, data, callback) {
        this._post('/api/classes/' + classId + '/update', data, callback);
    },

    createSchoolStudentAccount(data, callback) {
        this._post('/api/students/create-school-account', data, callback);
    },

    deactivateSchoolStudentAccount(studentId, callback) {
        this._post('/api/students/' + studentId + '/deactivate-school-account', { studentId }, callback);
    },

    reactivateSchoolStudentAccount(studentId, callback) {
        this._post('/api/students/' + studentId + '/reactivate-school-account', { studentId }, callback);
    },    

    getSchoolUserAccount(userId, callback) {
        this._get('/api/users/' + userId + '/school-account', callback);
    },

    createSchoolUserAccount(data, callback) {
        this._post('/api/users/create-school-account', data, callback);
    },

    updateSchoolUserAccount(data, callback) {
        this._post('/api/users/update-school-account', data, callback);
    },

    deactivateSchoolUserAccount(userId, callback) {
        this._post('/api/users/' + userId + '/deactivate-school-account', { userId }, callback);
    },

    reactivateSchoolUserAccount(userId, callback) {
        this._post('/api/users/' + userId + '/reactivate-school-account', { userId }, callback);
    },    

    deleteUserInfo(userId, callback) {
        const data = { userId };
        this._post('/api/users/' + userId + '/delete-info', data, callback);
    },

    mergeStudentGuardianAccounts(studentId, guardianId, callback) {
        const data = { studentId, guardianId };
        this._post('/api/users/merge-student-guardian-accounts', data, callback);
    },

    transferStudentAccountToSchool(studentId, schoolId, callback) {
        const data = { studentId, schoolId };
        this._post('/api/users/transfer-student-account-to-school', data, callback);
    },

    splitAdultStudentAccount(data, callback) {
        this._post('/api/users/split-adult-student-account', data, callback);
    },

    getTaskInfo(taskId, callback) {
        this._get('/api/tasks/' + taskId + '/info', callback);
    },

    deleteTask: function(taskId, callback) {
        const data = { taskId };
        this._post('/api/tasks/' + taskId + '/delete', data, callback);
    },

    transferTask: function(taskId, destinationStudentId, callback) {
        const data = { taskId, destinationStudentId };
        this._post('/api/tasks/' + taskId + '/transfer', data, callback);
    },

    /////////////////////////////////////////////////////////////////////////////////
    // Code Libraries

    getCodeLibraries(callback) {
        this._get('/api/code-libraries', callback);
    },

    getCodeLibrary(name, callback) {
        this._get('/api/code-libraries/' + name, callback);
    },

    saveCodeLibrary(name, code, callback) {
        let data = { name, code };
        this._post('/api/code-libraries/' + name, data, callback);
    },

    /////////////////////////////////////////////////////////////////////////////////
    // Version Upgrade

    acceptVersionUpgrade: function(studentId, courseId, callback) {
        let data = { studentId, courseId };
        this._post('/api/courses/' + courseId + '/accept-version-upgrade', data, callback);
    },

    declineVersionUpgrade: function(studentId, courseId, callback) {
        let data = { studentId, courseId };
        this._post('/api/courses/' + courseId + '/decline-version-upgrade', data, callback);
    },

    acknowledgeVersionUpgrade: function(studentId, courseId, callback) {
        let data = { studentId, courseId };
        this._post('/api/courses/' + courseId + '/acknowledge-version-upgrade', data, callback);
    },

    ////////////////////////////////////////////////////////////////////////////////
    // Dashboard

    /*
    getSchool: function (schoolId, callback) {
        this._get('/api/dashboard/schools/' + schoolId, callback);
    }, 

    addSchool(school, callback) {
        this._post('/api/dashboard/schools', school, callback);
    },

    updateSchool(school, callback) {
        this._post('/api/dashboard/schools/' + school.id + '/update', school, callback);
    },

    deleteSchool(schoolId, callback) {
        this._post('/api/dashboard/schools/' + schoolId + '/delete', null, callback);
    },
    */
   
    ////////////////////////////////////////////////////////////////////////////////

    postTaskEvents(taskId, data, callback) {
        this._post('/api/tasks/' + taskId + '/events', data, callback);
    },

    submitRequestProfile(data, callback) {
        this._post('/api/submit-request-profile', data, callback);
    },

    postTroubleshooting: function(taskId, entries, callback) {
        let data = { taskId, entries };
        this._post('/api/tasks/' + taskId + '/troubleshooting', data, callback);
    },
    updateProvidedSupport: function(customerId, providedSupport, callback) {
        let data = { customerId, providedSupport };
        this._post('/api/customers/' + customerId + '/provided-support', data, callback);
    },

    isEmailAvailable: function(email, callback) {
        let data = { email };
        this._post('/api/is-email-available', data, callback);
    },

    signUp: function(data, callback) {
        this._post('/api/sign-up', data, callback);
    },

    applyPromoCode(promoCode, callback) {
        var data = {
            promoCode
        };
        this._post('/api/apply-promo-code', data, callback);
    },

    getPaymentTaxAndTotal(data, callback) {
        this._post('/api/payment-tax-and-total', data, callback);
    },

    getIncompleteSubscriptions: function(callback) {
        this._get('/api/get-incomplete-subscriptions', callback);
    },

    getRequireActionSubscriptions: function(callback) {
        this._get('/api/get-require-action-subscriptions', callback);
    },

    getSubscription: function(subscriptionId, callback) {
        this._get('/api/get-subscription/' + subscriptionId, callback);
    },

    finalizeSignUp: function(callback) {
        this._post('/api/finalize-sign-up', null, callback);
    },  

    finalizeAddStudentAccount(data, callback) {
        this._post('/api/finalize-add-student-account', data, callback);
    },    

    cleanUpAfterFailedPayment: function(callback) {
        this._post('/api/clean-up-after-failed-payment', null, callback);
    },  

    setSubscriptionPaymentError: function(paymentError, callback) {
        var data = {
            paymentError
        };
        this._post('/api/set-subscription-payment-error', data, callback);
    },

    reportSubscriptionConfirmationResults: function(results, callback) {
        var data = {
            results
        };
        this._post('/api/report-subscription-confirmation-results', data, callback);
    },

    saveStudentAccount: function(studentAccount, callback) {
        this._post('/api/student-accounts/' + studentAccount.id, studentAccount, callback);
    },   
    
    reconfigureAccount: function(studentAccount, callback) {
        this._post('/api/reconfigure-account/' + studentAccount.id, { studentAccount }, callback);
    },   

    isStudentAccountEmailAvailable: function(studentAccountId, email, callback) {
        let data = { studentAccountId, email };
        this._post('/api/student-accounts/' + studentAccountId + '/is-email-available', data, callback);
    },

    initializeStudentAccounts: function(callback) {
        let data = {};
        this._post('/api/initialize-student-accounts', data, callback);
    },    

    initializePasswordReset: function(email, callback) {
        let data = { email };
        this._post('/api/initiate-password-reset', data, callback);
    },

    getStudent: function (studentId, callback) {
        this._get('/api/students/' + studentId, callback);
    },     

    getStudentCourse: function (studentId, courseId, callback) {
        this._get('/api/students/' + studentId + '/courses/' + courseId, callback);
    }, 

    updateStudentCourse: function(studentId, data, callback) {
        this._post('/api/students/' + studentId + '/course', data, callback);
    },

    getActiveStudentCourse: function(studentId, callback) {
        this._get('/api/students/' + studentId + '/course', callback);
    },

    resetStudentCourse: function(studentId, courseId, callback) {
        let data = { studentId, courseId };
        this._post('/api/students/' + studentId + '/courses/' + courseId + '/reset', data, callback);
    },

    resetKnowledgeProfile: function(studentId, callback) {
        this._post('/api/students/' + studentId + '/reset-knowledge-profile', {}, callback);
    },

    assignDiagnostic: function(studentId, courseId, callback) {
        let data = { studentId, courseId };
        this._post('/api/students/' + studentId + '/courses/' + courseId + '/assign-diagnostic', data, callback);
    },

    addStudentAccount: function(data, callback) {
        this._post('/api/student-accounts/new', data, callback);
    },

    reactivateStudentAccount(studentId, subscription, callback) {
        let data = { studentId, subscription };
        this._post('/api/student-accounts/reactivate', data, callback);
    },

    addGuardianAccount: function(data, callback) {
        this._post('/api/guardian-accounts/new', data, callback);
    },

    updatePaymentMethod: function(token, callback) {
        let data = { token };
        this._post('/api/update-payment-method', data, callback);        
    },

    upgradeSubscription: function(studentId, callback) {
        let data = { studentId };        
        this._post('/api/student-accounts/' + studentId + '/upgrade-subscription', data, callback);
    },

    upgradeSubscriptionToLifetime: function(studentId, callback) {
        let data = { studentId };        
        this._post('/api/student-accounts/' + studentId + '/upgrade-subscription-to-lifetime', data, callback);
    },

    finalizeUpgradeSubscription: function(studentId, callback) {
        let data = { studentId };        
        this._post('/api/student-accounts/' + studentId + '/finalize-upgrade-subscription', data, callback);
    },

    pauseSubscription: function(studentId, resumeOn, callback) {
        let data = { studentId, resumeOn };        
        this._post('/api/student-accounts/' + studentId + '/pause-subscription', data, callback);
    },

    cancelSubscription: function(studentId, reason, callback) {
        let data = { studentId, reason };
        this._post('/api/student-accounts/' + studentId + '/cancel-subscription', data, callback);
    },

    switchUserAccount: function(userIdentifier, callback) {
        let data = { userIdentifier };
        this._post('/api/switch-user-account', data, callback);
    },

    updateAccountAccess(studentId, guardianId, access, callback) {
        let data = { studentId, guardianId, access };
        this._post('/api/student-accounts/' + studentId + '/update-account-access', data, callback);
    },

    removeAccountAccess(studentId, guardianId, callback) {
        let data = { studentId, guardianId };
        this._post('/api/student-accounts/' + studentId + '/remove-account-access', data, callback);
    },    

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Student XP Goals

    getStudentXPGoals: function (studentId, callback) {
        this._get('/api/students/' + studentId + '/xp-goals', callback);
    },  

    updateStudentXPGoals: function(studentId, data, callback) {
        this._post('/api/students/' + studentId + '/xp-goals', data, callback);
    },

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Student Accommodations

    getStudentAccommodations: function (studentId, callback) {
        this._get('/api/students/' + studentId + '/accommodations', callback);
    },  

    updateStudentAccommodations: function(studentId, data, callback) {
        this._post('/api/students/' + studentId + '/accommodations', data, callback);
    },

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Student Classes

    sendClassInvitations: function(classId, emails, callback) {
        const data = { classId, emails };
        this._post('/api/classes/' + classId + '/send-invitations', data, callback);
    },

    joinClass: function(studentId, classCode, callback) {
        const data = { studentId, classCode };
        this._post('/api/students/' + studentId + '/join-class', data, callback);
    },

    leaveClass: function(studentId, classId, callback) {
        const data = { studentId, classId };
        this._post('/api/students/' + studentId + '/leave-class', data, callback);
    },      

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // PopupNotification
    
    confirmPopupNotification: function(popupNotificationId, callback) {
        let data = { popupNotificationId };
        this._post('/api/popup-notifications/' + popupNotificationId + '/confirm', data, callback);
    },

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Multistep

    getMultistepType: function (multistepTypeId, callback) {
        this._get('/api/multistep-types/' + multistepTypeId, callback);
    },    
    createMultistepType: function(courseId, name, description, callback) {
        let data = { courseId, name, description };
        this._post('/api/multistep-types/new', data, callback);
    },
    updateMultistepType: function(id, name, description, callback) {
        let data = { id, name, description };
        this._post('/api/multistep-types/' + id + '/update', data, callback);
    },    
    updateMultistepTypeLive: function(id, live, callback) {
        let data = { id, live };
        this._post('/api/multistep-types/' + id + '/update-live', data, callback);
    },      
    deleteMultistepType: function(id, callback) {
        let data = { id };
        this._post('/api/multistep-types/' + id + '/delete', data, callback);
    },   
    getMultistep: function (multistepId, process, callback) {
        let url = '/api/multisteps/' + multistepId;
        if (process) {
            url += '?process=true'
        }

        this._get(url, callback);
    },        
    getMultistepSteps: function (multistepId, callback) {
        this._get('/api/multisteps/' + multistepId + '/steps', callback);
    },
    getMultistepTutorial: function (multistepId, tutorialId, callback) {
        this._get('/api/multisteps/' + multistepId + '/tutorials/' + tutorialId, callback);
    },
    insertMultistepTutorialStep: function (multistepId, stepNumber, title, content, graphics, callback) {
        let data = { stepNumber, title, content, graphics };
        this._post('/api/multisteps/' + multistepId + '/insert-tutorial-step', data, callback);
    },
    updateMultistepTutorial: function (multistepId, tutorialId, content, graphics, callback) {
        let data = { content, graphics };
        this._post('/api/multisteps/' + multistepId + '/tutorials/' + tutorialId + '/update', data, callback);
    },
    updateMultistepTutorialTitle: function (multistepId, tutorialId, title, callback) {
        let data = { title };
        this._post('/api/multisteps/' + multistepId + '/tutorials/' + tutorialId + '/update-title', data, callback);
    },
    deleteMultistepTutorialStep: function (multistepId, stepNumber, callback) {
        let data = { stepNumber };
        this._post('/api/multisteps/' + multistepId + '/delete-tutorial-step', data, callback);
    },
    transposeMultistepSteps: function (multistepId, projectStepId1, projectStepId2, callback) {
        let data = { projectStepId1, projectStepId2 };
        this._post('/api/multisteps/' + multistepId + '/transpose-steps', data, callback);
    },
    createMultistep: function (multistepTypeId, text, graphics, callback) {
        let data = { multistepTypeId, text, graphics };
        this._post('/api/multisteps/new', data, callback);
    },
    updateMultistep: function (multistepId, text, graphics, callback) {
        let data = { multistepId, text, graphics };
        this._post('/api/multisteps/' + multistepId, data, callback);
    },   
    deleteMultistep: function (multistepId, callback) {
        let data = {};
        this._post('/api/multisteps/' + multistepId + '/delete', data, callback);
    },     
    cloneMultistep: function (multistepId, callback) {
        let data = {};
        this._post('/api/multisteps/' + multistepId + '/clone', data, callback);
    }, 
    submitMultistep: function (multistepId, callback) {
        let data = { multistepId };
        this._post('/api/multisteps/' + multistepId + '/submit', data, callback);
    },
    unsubmitMultistep: function (multistepId, callback) {
        let data = { multistepId };
        this._post('/api/multisteps/' + multistepId + '/unsubmit', data, callback);
    },    
    acceptMultistep: function (multistepId, callback) {
        let data = { multistepId };
        this._post('/api/multisteps/' + multistepId + '/accept', data, callback);
    },
    unacceptMultistep: function (multistepId, callback) {
        let data = { multistepId };
        this._post('/api/multisteps/' + multistepId + '/unaccept', data, callback);
    },    
    deleteMultistepQuestion: function (multistepId, questionId, stepNumber, callback) {
        let data = { multistepId, questionId, stepNumber };
        this._post('/api/multisteps/' + multistepId + '/questions/' + questionId + '/delete', data, callback);
    },
    transposeMultistepQuestions: function (multistepId, question1Id, question2Id, callback) {
        let data = { multistepId, question1Id, question2Id };
        this._post('/api/multisteps/' + multistepId + '/transpose-questions', data, callback);
    },
    updateMultistepQuestionKP: function (multistepTypeId, stepNumber, topicId, exampleId, callback) {
        var data = { multistepTypeId, stepNumber, topicId, exampleId };        
        this._post('/api/multistep-types/' + multistepTypeId + '/step-knowledge-point', data, callback);        
    },
    updateMultistepQuestionDifficulty: function (multistepTypeId, stepNumber, difficulty, callback) {
        var data = { multistepTypeId, stepNumber, difficulty };        
        this._post('/api/multistep-types/' + multistepTypeId + '/step-difficulty', data, callback);        
    },
    getTaskMultistepState(taskId, multistepId, callback) {
        this._get('/api/tasks/' + taskId + '/multisteps/' + multistepId + '/state', callback);
    },
    selectTaskQuestion(taskId, questionId, callback) {
        var data = { taskId, questionId };
        this._post('/api/tasks/' + taskId + '/questions/' + questionId + '/select-question', data, callback);
    },
    submitMultistepAnswer(taskId, multistepId, data, callback) {
        this._post('/api/tasks/' + taskId + '/multisteps/' + multistepId + '/submit-answer', data, callback);
    },

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Tasks
    getIncompleteDiagnosticTask(studentId, courseId, callback) {
        this._get('/api/students/' + studentId + '/courses/' + courseId + '/incomplete-diagnostic-task', callback);
    },
    getIncompleteTasks(studentId, courseId, callback) {
        this._get('/api/students/' + studentId + '/courses/' + courseId + '/incomplete-tasks', callback);
    },
    generateNewTasks: function(callback) {
        let data = {};
        this._post('/api/tasks/generate', data, callback);
    },
    getNewTasks: function(callback) {
        this._get('/api/new-tasks', callback);
    },
    getPreviousTasks(date, callback, minumum = 25) {
        this._get(`/api/previous-tasks/${date}${minumum != 25 ? `?minumum=${minumum}` : '' }`, callback);
    },

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Animation

    getAnimation: function(animationId, callback) {
        this._get('/api/animations/' + animationId, callback);
    },
    createAnimation: function (data, callback) {
        this._post('/api/animations/new', data, callback);
    },
    updateAnimation: function (data, callback) {
        this._post('/api/animations/' + data.id, data, callback);
    },

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Diagnostic

    getNextDiagnosticQuestion(diagnosticId, taskId, retry, callback) {
        this._get('/api/diagnostics/' + diagnosticId + '/next-question?taskId=' + taskId + '&retry=' + retry, callback);
    },

    submitDiagnosticAnswer: function (diagnosticId, data, callback) {
        this._post('/api/diagnostics/' + diagnosticId, data, callback);
    },

    getDiagnosticAnalysis(diagnosticId, taskId, callback) {
        this._get('/api/diagnostics/' + diagnosticId + '/analysis?taskId=' + taskId, callback);
    },

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Performance

    getClassPerformanceDate(sectionId, period, callback) {
        this._get('/api/classes/' + sectionId + '/performance?period=' + period, callback);
    },
    getCoursePerformanceDate(courseId, period, callback) {
        this._get('/api/courses/' + courseId + '/performance?period=' + period, callback);
    },

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Bookmark
    createBookmark(contentType, contentId, notes, callback) {
        var data = { contentType, contentId, notes };
        this._post('/api/bookmarks/new', data, callback);
    },
    deleteBookmark(bookmarkId, callback) {
        var data = { bookmarkId };
        this._post('/api/bookmarks/' + bookmarkId + '/delete', data, callback);
    },
    
    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Courses
    getNewVersionOfCourse(courseId, callback) {
        this._get('/api/courses/' + courseId + '/new-version', callback);
    }, 
    getCourses(callback) {
        this._get('/api/courses', callback);
    }, 
    getCoursesByCategory(locale, callback) {
        let url = '/api/courses-by-category';

        if (locale) {
            url += '?locale=' + locale;
        }

        this._get(url, callback);
    },     
    getCoursesByCategoryWithDevelopment(locale, callback) {
        let url = '/api/courses-by-category-with-development';

        if (locale) {
            url += '?locale=' + locale;
        }

        this._get(url, callback);
    },     
    getCourseContent(courseId, callback) {
        this._get('/api/courses/' + courseId + '/content', callback);
    },
    getStudentCourseContent(studentId, courseId, callback) {
        this._get('/api/courses/' + courseId + '/students/' + studentId + '/content', callback);
    },
    getCourseKnowledgeGraph: function (courseIds, callback) {
        this._get('/api/courses/' + courseIds + '/knowledge-graph', callback);
    },   
    getCourseKnowledgeGraphSVG: function (courseIds, callback) {
        this._get('/api/courses/' + courseIds + '/knowledge-graph-svg', callback);
    },   
    getStudentCourseKnowledgeGraph: function(studentId, courseIds, callback) {
        let courseIdList = courseIds.join(',');
        this._get('/api/courses/' + courseIdList + '/students/' + studentId + '/knowledge-graph', callback);
    },       
    updateCourseKnowledgeGraphSVG: function(courseId, graphSVG, callback) {
        let data = { courseId, graphSVG };
        this._post('/api/courses/' + courseId + '/knowledge-graph-svg', data, callback);
    },
    getUnitKnowledgeGraph: function (unitId, callback) {
        this._get('/api/units/' + unitId + '/knowledge-graph', callback);
    },   

    getClassCourseProgress: function(sectionId, courseId, callback) {
        this._get('/api/courses/' + courseId + '/sections/' + sectionId + '/progress', callback);
    },   
    getStudentCourseProgress: function(studentId, courseId, callback) {
        this._get('/api/courses/' + courseId + '/students/' + studentId + '/progress', callback);
    },  
    getStudentCourseStatus(studentId, courseId, callback) {
        this._get('/api/courses/' + courseId + '/students/' + studentId + '/status', callback);
    },
    getClassCourses: function(classId, callback) {
        this._get('/api/classes/' + classId + '/courses', callback);
    },     
    getStudentCurrentCourse: function(studentId, callback) {
        this._get('/api/students/' + studentId + '/current-course', callback);
    },     

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Examples
    getTopicExamples(topicId, callback) {
        this._get('/api/topics/' + topicId + '/examples', callback);
    },     

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Topics 

    getTopicMetaData: function (topicId, callback) {
        this._get('/api/topics/' + topicId + '/meta-data', callback);
    },  
    getTopicInfo: function (topicId, callback) {
        this._get('/api/topics/' + topicId + '/name', callback);
    },
    getQuestionTopics(questionIds, callback) {
        this._post('/api/questions/data', {questionIds: questionIds}, callback);
    },
    acceptTopic: function (topicId, callback) {
        this._post('/api/topics/' + topicId + '/accept', null, callback);
    },
    unacceptTopic: function (topicId, callback) {
        this._post('/api/topics/' + topicId + '/unaccept', null, callback);
    },
    submitTopic: function (topicId, callback) {
        this._post('/api/topics/' + topicId + '/submit', {}, callback);
    },
    unsubmitTopic: function (topicId, callback) {
        this._post('/api/topics/' + topicId + '/unsubmit', null, callback);
    },
    checkAssignedQuestionsCount: function (topicId, callback) {
        this._get('/api/topics/' + topicId + '/assigned-questions', callback);
    },
    getTopicPrerequisites(topicId, callback) {
        this._get('/api/topics/' + topicId + '/prerequisites', callback);
    },    
    updateTopicPrerequisites(topicId, prerequisiteTopicIds, callback) {
        var data = {topicId: topicId, prerequisites: prerequisiteTopicIds};
        this._post('/api/topics/' + topicId + '/prerequisites', data, callback);
    },    
    showPrerequisiteGraph(courseId, callback) {
        this._get('/api/topics/' + courseId + '/prequisite-graph', callback);
    },
    publishTopic: function (topicId, callback) {
        this._post('/api/topics/' + topicId + '/publish', null, callback);
    },
    unpublishTopic: function (topicId, callback) {
        this._post('/api/topics/' + topicId + '/unpublish', null, callback);
    },
    editTutorialContent: function(topicId, callback) {
      this._get('/api/topic/' + topicId + '/edit-tutorial', callback);
    },
    updateTutorialContent: function(topicId, data, callback) {
        this._post('/api/topic/' + topicId + '/updateTutorial', data, callback);
    },
    sendTutorialFeedback: function(data, callback) {
        this._post('/api/send-tutorial-feedback', data, callback);
    },
    getTopicsPath: function(topics, callback) {
        this._post('/api/get-topics-path', {topics}, callback);
    },
    changeTopicStatus(topicId, status, callback) {
        this._post('/api/change-topic-status', {topicId, status}, callback);
    },
    setTopicLive(topicId, live, callback) {
        var data = { topicId: topicId, live: live };
        this._post('/api/topics/' + topicId + '/live', data, callback);
    },
    setTopicOptional(courseId, topicId, optional, callback) {
        var data = { courseId: courseId, topicId: topicId, optional: optional };
        this._post('/api/courses/' + courseId + '/topics/' + topicId + '/optional', data, callback);
    },
    setExampleOptional(courseId, exampleId, optional, callback) {
        var data = { courseId: courseId, exampleId: exampleId, optional: optional };
        this._post('/api/courses/' + courseId + '/examples/' + exampleId + '/optional', data, callback);
    },

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Question Groups
    createQuestionGroup: function(data, callback) {
        this._post('/api/question-groups/new', data, callback);
    },
    updateQuestionGroup: function(data, callback) {
        this._post('/api/question-groups/' + data.id + '/update', data, callback);
    },    
    transposeQuestionGroups: function(questionGroup1Id, questionGroup2Id, callback) {
        let data = { questionGroup1Id, questionGroup2Id };
        this._post('/api/question-groups/transpose', data, callback);
    },
    removeQuestionGroup: function(questionGroupId, callback) {
        let data = { questionGroupId };
        this._post('/api/question-groups/' + questionGroupId + '/remove', data, callback);
    },    
    updateQuestionGroupTarget: function(questionGroupId, target, modelType, callback) {
        let data = { questionGroupId, target, modelType };        
        this._post('/api/question-groups/' + questionGroupId + '/update-target', data, callback);
    },    

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Questions
    createQuestion: function (data, callback) {
        this._post('/api/questions/new', data, callback);
    },
    updateQuestion: function (data, callback) {
        this._post('/api/questions/' + data.id, data, callback);
    },
    updateQuestionType: function (questionId, questionType, callback) {
        var data = { questionId, questionType };
        this._post('/api/questions/' + questionId + '/type', data, callback);
    },
    moveQuestion: function (questionId, oldTopicId, newTopicId, callback) {
        var data = {questionId: questionId, oldTopicId: oldTopicId, newTopicId: newTopicId};
        this._post('/api/questions/' + questionId + '/move-to-topic', data, callback);
    },
    moveQuestionToExample: function(questionId, exampleId, callback) {
        let data = { questionId, exampleId };        
        this._post('/api/questions/' + questionId + '/move-to-example', data, callback);
    },         
    moveQuestionToGroup: function(questionId, exampleId, groupId, callback) {
        let data = { questionId, exampleId, groupId };        
        this._post('/api/questions/' + questionId + '/move-to-group', data, callback);
    },         
    deleteQuestion: function (questionId, callback) {
        this._post('/api/questions/' + questionId + '/delete', null, callback);
    },
    restoreQuestion: function (questionId, callback) {
        this._post('/api/questions/' + questionId + '/restore', null, callback);
    },    
    recheckQuestion: function (questionId, callback) {
        this._post('/api/questions/' + questionId + '/recheck', null, callback);
    },    
    submitQuestion: function (questionId, callback) {
        var data = {questionId: questionId};
        this._post('/api/questions/' + questionId + '/submit', data, callback);
    },
    acceptQuestion: function (questionId, callback) {
        var data = { questionId };
        this._post('/api/questions/' + questionId + '/accept', data, callback);
    },
    acceptQuestions: function (questionIds, callback) {
        var data = { questionIds };
        this._post('/api/questions/accept', data, callback);
    },    
    updateQuestionDifficulty: function (questionId, difficulty, callback) {
        var data = {questionId: questionId, difficulty: difficulty};
        this._post('/api/questions/' + questionId + '/difficulty', data, callback);
    },
    getGroupQuestions: function (groupId, callback) {
        this._get('/api/question-groups/' + groupId + '/questions', callback);
    },
    getUncategorizedQuestions: function (topicId, callback) {
        this._get('/api/topics/' + topicId + '/questions/uncategorized', callback);
    },

    getExample: function (exampleId, callback) {
        this._get('/api/examples/' + exampleId, callback);
    },
    getQuestion: function (questionId, callback) {
        this._get('/api/questions/' + questionId, callback);
    },
    getGroupQuestionsBasic: function (groupId, callback) {
        this._get('/api/groups/' + groupId + '/questions', callback);
    },
    getQuestionComplete: function (questionId, callback) {
        this._get('/api/questions/' + questionId + '/complete', callback);
    },
    getQuestionStatus: function (questionId, callback) {
        this._get('/api/questions/' + questionId + '/status', callback);
    },
    getQuestionStats: function (questionId, callback) {
        this._get('/api/questions/' + questionId + '/stats', callback);
    },
    getQuestions(status, offset, callback) {
        this._get('/api/questions?status=' + status + '&offset=' + offset, callback);
    },
    getMostDifficultQuestions(offset, callback) {
        this._get('/api/most-difficult-question?offset=' + offset, callback)
    },
    skipQuestion: function (question, callback) {
        this._post('/api/assignments/' + question.assignmentId + '/questions/' + question.questionId, question, callback);
    },
    getTopicQuestions: function (topicId, callback) {
        this._get('/api/topics/' + topicId + '/questions', callback);
    },
    getTopicQuestionsMetaData: function(topicId, callback) {
        this._get('/api/topics/' + topicId + '/questions/meta', callback);
    },
    getExemplarQuestions: function (topicId, limit = null, callback) {
        this._get('/api/topics/' + topicId + '/exemplar-questions?limit=' + limit, callback);
    },
    getAuthorQuestions: function (authorId, offset, callback) {
        this._get('/authors/' + authorId + '/questions?offset=' + offset, callback);
    },
    getNextAssignmentQuestion: function (assignmentId, callback) {
        this._get('/api/assignments/' + assignmentId + '/next-question', callback);
    },
    getNextReviewQuestion: function (taskId, callback) {
        this._get('/api/tasks/' + taskId + '/next-review-question', callback);
    },    
    getTestQuestionById: function (testId, questionId, callback) {
        this._get('/api/tests/' + testId + '/next-question/' + questionId, callback);
    },

    getAssignmentQuestion: function (questionId, callback) {
        this._get('/api/assignment-questions/' + questionId, callback);
    },

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Flags
    flagQuestion: function (data, callback) {
        this._post('/api/questions/' + data.questionId + '/flag', data, callback);
    },
    resolveQuestionFlags: function (questionId, callback) {
        this._post('/api/questions/' + questionId + '/resolve-flags', null, callback);
    },
    getQuestionFlag: function (questionId, callback) {
        this._get('/api/questions/' + questionId + '/flag', callback);
    },
    getFlaggedQuestions(offset, callback) {
        this._get('/api/flagged-questions?offset=' + offset, callback);
    },
    getFlags: function(offset, callback) {
        this._get('/api/resolved-flags?offset=' + offset, callback);
    },
    getUresolvedFlags: function(offset, callback) {
      this._get('/api/unresolved-flags?offset=' + offset, callback);
    },

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Comments
    submitQuestionComment: function (questionId, content, callback) {
        var data = {questionId: questionId, content: content};
        this._post('/api/questions/' + questionId + '/comment/new', data, callback);
    },
    submitTopicComment: function (topicId, topicName, content, callback) {
        var data = {topicId: topicId, topicName: topicName, content: content};
        this._post('/api/topics/' + topicId + '/comments', data, callback);
    },
    updateComment: function (commentId, content, callback) {
        var data = {commentId: commentId, content: content};
        this._post('/api/comments/' + commentId + '/edit', data, callback);
    },
    deleteComment: function (commentId, callback) {
        var data = {commentId: commentId};
        this._post('/api/topics/comment/delete', data, callback);
    },
    archiveComment: function (commentId, callback) {
        var data = {commentId: commentId};
        this._post('/api/topics/comment/archive', data, callback);
    },
    getComment: function (commentId, callback) {
        this._get('/api/comments/' + commentId, callback);
    },
    getComments(offset, callback) {
        this._get('/api/comments?offset=' + offset, callback);
    },
    getAuthorComments(authorId, offset, callback) {
        this._get('/api/authors/' + authorId + '/comments?offset=' + offset, callback);
    },
    getArchivedComments(offset, callback) {
        this._get('/api/archived-comments?offset=' + offset, callback);
    },
    getTopicComments(topicId, offset, callback) {
        this._get('/api/topics/' + topicId + '/comments?offset=' + offset, callback);
    },
    getCourseComments(courseId, offset, callback) {
        this._get('/api/courses/' + courseId + '/comments?offset=' + offset, callback);
    },
    unArchiveComment(commentId, callback) {
        this._post('/api/comments/' + commentId + '/unarchive', callback);
    },

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Graphics


    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Documents
    getDocument: function(documentId, callback) {
        this._get('/api/dashboard/documents/' + documentId, callback);
    },
    getDocumentRevisions: function(documentId, callback) {
        this._get('/api/dashboard/documents/' + documentId + '/revisions', callback);
    },
    createDocument: function (data, callback) {
        this._post('/api/dashboard/documents/new', data, callback);
    },    
    updateDocument: function (documentId, data, callback) {
        this._post('/api/dashboard/documents/' + documentId, data, callback);
    },    
    updateDocumentContent: function (documentId, data, callback) {
        this._post('/api/dashboard/documents/' + documentId + '/content', data, callback);
    },       
    deleteDocument: function (documentId, callback) {
        this._post('/api/dashboard/documents/' + documentId + '/delete', null, callback);
    },
    publishDocument: function (documentId, callback) {
        this._post('/api/dashboard/documents/' + documentId + '/publish', null, callback);
    },    
    unpublishDocument: function (documentId, callback) {
        this._post('/api/dashboard/documents/' + documentId + '/unpublish', null, callback);
    },   
    publishDocumentLastRevision: function (documentId, callback) {
        this._post('/api/dashboard/documents/' + documentId + '/publish-last-revision', null, callback);
    },    
    discardDocumentLastRevision: function (documentId, callback) {
        this._post('/api/dashboard/documents/' + documentId + '/discard-last-revision', null, callback);
    },    
    getCollections: function(callback) {
        this._get('/api/dashboard/collections', callback);
    },
    createCollection: function (data, callback) {
        this._post('/api/dashboard/collections/new', data, callback);
    },    
    updateCollection: function (collectionId, data, callback) {
        this._post('/api/dashboard/collections/' + collectionId, data, callback);
    },    
    deleteCollection: function (collectionId, callback) {
        this._post('/api/dashboard/collections/' + collectionId + '/delete', null, callback);
    },

    saveObject: function (objectPath, data, callback) {
        let url = this._join('/api/', objectPath);
        url += '/' ;
        url += data.id ? data.id : 'new';

        this._post(url, data, callback);
    },    

    // WTF: We have a generateExplanationGraphic endpoint, why is the 'OrExplanation' about?
    generateGraphic: function (questionId, fieldName, tex, version, callback) {
        var data = {
            questionId,
            fieldName,
            tex
        };

        if (version === 2) {
            this._post('/api/graphics/create', data, callback);
        } else {
            this._post('/api/generate-graphic', data, callback);
        }
    },

    // WTF: Why are explanation and dialog parameters?
    generateCommentGraphic: function (commentId, graphicIndex, tex, text, callback) {
        var data = {
            commentId: commentId,
            graphicIndex: graphicIndex,
            tex: tex,
            fullText: text
        };

        this._post('/api/generate-comment-graphic', data, callback);
    },

    // More general version can cover (tutorial, and lessonStep)
    generateGraphic_NEW: function(fileId, tex, callback) {
        var data = { 
            fileId: fileId,
            tex: tex
        };
        this._post('/api/generate-graphic-new', data, callback);
    },


    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Key Prerequisites

    getKeyPrerequisites(knowledgePointId, callback) {
        this._get('/api/knowledge-points/' + knowledgePointId + '/key-prerequisites', callback);
    },
    updateKeyPrerequisites(knowledgePointId, prerequisiteIds, callback) {
        var data = { knowledgePointId, prerequisiteIds };
        this._post('/api/knowledge-points/' + knowledgePointId + '/key-prerequisites', data, callback);
    },

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Lessons
    selectLessonStep(taskId, topicId, lessonStructure, stepNumber, questionId, callback) {
        var data = { taskId, topicId, lessonStructure, stepNumber, questionId };
        this._post('/api/tasks/' + taskId + '/lessons/' + topicId + '/select-step', data, callback);
    },
    submitLessonAnswer(taskId, topicId, data, callback) {
        this._post('/api/tasks/' + taskId + '/lessons/' + topicId + '/submit-answer', data, callback);
    },
    getTaskAnswers(taskId, callback) {
        this._get('/api/tasks/' + taskId + '/answers', callback);
    },

    getStudentCourseLesson(taskId, topicId, callback) {
        this._get('/api/tasks/' + taskId + '/lessons/' + topicId, callback);
    },
    resetPracticeQuestions(topicId, callback) {
        var data = {topicId: topicId};
        this._post('/api/topics/' + topicId + '/reset-practice-questions', data, callback);
    },
    getReferenceLesson(topicId, callback) {
        this._get('/api/lessons/' + topicId, callback);
    },
    getTaskLessonState(taskId, topicId, callback) {
        this._get('/api/tasks/' + taskId + '/lessons/' + topicId + '/state', callback);
    },
    getTaskReviewState(taskId, topicId, callback) {
        this._get('/api/tasks/' + taskId + '/review/' + topicId + '/state', callback);
    },
    getTaskDrillState(taskId, topicId, callback) {
        this._get('/api/tasks/' + taskId + '/drills/' + topicId + '/state', callback);
    },    
    
    cleanupTaskData(taskId, callback) {
        var data = {taskId: taskId};
        this._post('/api/tasks/' + taskId + '/cleanup', data, callback);
    },

    insertLesson(topicId, callback) {
        var data = {topicId: topicId};
        this._post('/api/topics/' + topicId + '/lessons', data, callback);
    },

    exportContext(topicId, data, callback) {
        this._post('/api/topics/' + topicId + '/export-context', data, callback);
    },

    exportLesson(topicId, includeImagesAndTables, callback) {
        var url = '/api/topics/' + topicId + '/export-lesson';
        if (includeImagesAndTables) {
            url += '?includeImagesAndTables=true';
        }
        this._get(url, callback);
    },

    importQuestions(topicId, data, callback) {
        this._post('/api/topics/' + topicId + '/import-questions', data, callback);
    },

    importLesson(topicId, data, callback) {
        this._post('/api/topics/' + topicId + '/import-lesson', data, callback);
    },
    importLessons(data, callback) {
        this._post('/api/import-lessons', data, callback);
    },  
    
    importProject(courseId, data, callback) {
        this._post('/api/courses/' + courseId + '/import-project', data, callback);
    },    

    deleteLesson(topicId, callback) {
        var data = { topicId };
        this._post('/api/topics/' + topicId + '/delete-lesson', data, callback);
    },
    insertLessonStepTutorial: function(topicId, lessonId, number, content, graphics, callback) {
        var data = {topicId, lessonId: lessonId, number: number, content: content, graphics: graphics};
        this._post('/api/lessons/' + lessonId + '/insert-tutorial-step', data, callback);
    },
    insertLessonStepExample: function(topicId, lessonId, number, question, explanation, graphics, callback) {
        var data = {topicId, lessonId, number, question, explanation, graphics};
        this._post('/api/lessons/' + lessonId + '/insert-example-step', data, callback);
    },
    insertLessonStepQuestion: function(lessonId, number, questionId, exampleId, callback) {
        var data = {lessonId: lessonId, number: number, questionId: questionId, exampleId: exampleId};
        this._post('/api/lessons/' + lessonId + '/insert-question-step', data, callback);
    },
    cloneLessonStepQuestion(lessonId, number, questionId, callback) {
        var data = {lessonId: lessonId, number: number, questionId: questionId};
        this._post('/api/lessons/' + lessonId + '/clone-question-step', data, callback);
    },   
    transposeLessonSteps: function(lessonId, stepId1, stepId2, callback) {
        var data = {lessonId: lessonId, stepId1: stepId1, stepId2: stepId2 };
        this._post('/api/lessons/' + lessonId + '/transpose-steps', data, callback);
    },
    deleteLessonStep: function(lessonId, stepId, type, contentId, number, callback) {
        var data = {lessonId: lessonId, stepId: stepId, type: type, contentId: contentId, number: number};
        this._post('/api/lessons/' + lessonId + '/delete-step', data, callback);
    },

    submitLesson: function(lessonId, callback) {
        var data = { lessonId };
        this._post('/api/lessons/' + lessonId + '/submit', data, callback);
    },
    acceptLesson: function(lessonId, forceReason, callback) {
        var data = { lessonId, forceReason };
        this._post('/api/lessons/' + lessonId + '/accept', data, callback);
    },  

    submitTopic: function(topicId, lessonId, callback) {
        var data = { topicId, lessonId };
        this._post('/api/topics/' + topicId + '/submit', data, callback);
    },
    acceptTopic: function(topicId, forceReason, callback) {
        var data = { topicId, forceReason };
        this._post('/api/topics/' + topicId + '/accept', data, callback);
    },      

    submitTopicTutorialsAndExamples: function(topicId, callback) {
        var data = { topicId };
        this._post('/api/topics/' + topicId + '/submit-tutorials-and-examples', data, callback);
    },

    submitTutorial: function(tutorialId, callback) {
        var data = { tutorialId };
        this._post('/api/tutorials/' + tutorialId + '/submit', data, callback);
    },
    acceptTutorial: function(tutorialId, forceReason, callback) {
        var data = { tutorialId, forceReason };
        this._post('/api/tutorials/' + tutorialId + '/accept', data, callback);
    },    
    submitExample: function(exampleId, callback) {
        var data = { exampleId };
        this._post('/api/examples/' + exampleId + '/submit', data, callback);
    },
    acceptExample: function(exampleId, forceReason, callback) {
        var data = { exampleId, forceReason };
        this._post('/api/examples/' + exampleId + '/accept', data, callback);
    }, 

    // OLD versions
    //
    getLessonStepTutorial: function(lessonId, tutorialId, callback) {
        this._get('/api/lessons/' + lessonId + '/tutorials/' + tutorialId, callback);
    },
    updateLessonStepTutorial: function(lessonId, tutorialId, content, graphics, callback) {
        var data = {lessonId: lessonId, tutorialId: tutorialId, content: content, graphics: graphics};
        this._post('/api/lessons/' + lessonId + '/update-tutorial', data, callback);
    },
    getLessonStepExample: function(lessonId, exampleId, callback) {
        this._get('/api/lessons/' + lessonId + '/examples/' + exampleId, callback);
    },
    updateLessonStepExample: function(lessonId, exampleId, question, explanation, graphics, callback) {
        var data = {lessonId: lessonId, exampleId: exampleId, question: question, explanation: explanation, graphics: graphics};
        this._post('/api/lessons/' + lessonId + '/update-example', data, callback);
    },
    updateLessonStepTutorialTitle: function(lessonId, tutorialId, title, callback) {
        var data = {lessonId: lessonId, tutorialId: tutorialId, title: title};
        this._post('/api/lessons/' + lessonId + '/update-tutorial-title', data, callback);
    },    
    updateLessonStepExampleTitle: function(lessonId, exampleId, title, callback) {
        var data = {lessonId: lessonId, exampleId: exampleId, title: title};
        this._post('/api/lessons/' + lessonId + '/update-example-title', data, callback);
    },       

    
    // NEW versions
    //
    getLesson: function(topicId, callback) {
        this._get('/api/topics/' + topicId + '/lesson', callback);
    },
    getTutorial: function(tutorialId, callback) {
        this._get('/api/tutorials/' + tutorialId, callback);
    },
    updateTutorial: function(tutorialId, content, graphics, callback) {
        var data = { tutorialId, content, graphics };
        this._post('/api/tutorials/' + tutorialId + '/update', data, callback);
    },
    updateTutorialTitle: function(tutorialId, title, callback) {
        var data = { tutorialId, title };
        this._post('/api/tutorials/' + tutorialId + '/update-title', data, callback);
    },        
    getExample: function(exampleId, callback) {
        this._get('/api/examples/' + exampleId, callback);
    },
    updateExample: function(exampleId, question, explanation, graphics, callback) {
        var data = {exampleId, question, explanation, graphics};
        this._post('/api/examples/' + exampleId + '/update', data, callback);
    },
    updateExampleTitle: function(exampleId, title, callback) {
        var data = { exampleId, title };
        this._post('/api/examples/' + exampleId + '/update-title', data, callback);
    },       

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Classes / Sections

    getStudentsStats: function(sectionId, callback) {
      this._get('/api/classes/' + sectionId + '/get-students-stats', callback);
    },
    disableStudent: function (sectionId, studentId, value, callback) {
        this._post('/api/classes/' + sectionId + '/students/' + studentId + '/changeStatus', {value: value}, callback);
    },
    getClassPriorityTopicsByCourse: function(classId, courseIds, callback) {
        const courseIdList = courseIds.join(',');
        this._get('/api/classes/' + classId + '/courses/' + courseIdList + '/priority-topics', callback);
    },    
    getClassPriorityTopics: function(classId, callback) {
        this._get('/api/classes/' + classId + '/priority-topics', callback);        
    },
    addClassPriorityTopic: function(sectionId, topicId, callback) {
        let data = { sectionId, topicId };
        this._post('/api/sections/' + sectionId + '/topics/' + topicId + '/add-priority-topic', data, callback);
    },
    getStudentPriorityTopics: function(studentId, callback) {
        this._get('/api/students/' + studentId + '/priority-topics', callback);        
    },
    removeClassPriorityTopic: function(sectionId, topicId, callback) {
        let data = { sectionId, topicId };
        this._post('/api/sections/' + sectionId + '/topics/'+ topicId + '/remove-priority-topic', data, callback);
    },   
    updateClassPriorityTopics: function(sectionId, priorityTopicIds, callback) {
        let data = { sectionId, priorityTopicIds };
        this._post('/api/sections/' + sectionId + '/update-priority-topics', data, callback);
    },   
    updateStudentPriorityTopics: function(studentId, priorityTopicIds, callback) {
        let data = { studentId, priorityTopicIds };
        this._post('/api/students/' + studentId + '/update-priority-topics', data, callback);
    },         

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Assignments
    getNewAssignmentInfo: function (sectionId, callback) {
        this._get('/api/classes/' + sectionId + '/assignments/new', callback);
    },
    getEditAssignmentInfo: function(sectionId, assignmentId, callback) {
        this._get('/api/classes/' + sectionId + '/assignments/' + assignmentId + '/edit', callback);
    },
    createAssignment: function (data, callback) {
        this._post('/api/classes/' + data.sectionId + '/assignments/new', data, callback);
    },
    editAssignment: function (data, callback) {
        this._post('/api/classes/' + data.sectionId + '/assignments/' + data.assignmentId + '/edit', data, callback);
    },
    resetAssignment: function (assignmentId, studentId, callback) {
        this._post('/api/assignments/' + assignmentId + '/students/' + studentId + '/reset', null, callback);
    },
    markAsComplete: function (assignmentId, studentId, callback) {
        this._post('/api/assignments/' + assignmentId + '/students/' + studentId + '/markAsComplete', null, callback);
    },
    getAssignmentPassingInfo: function(assignmentId, callback) {
      this._get('/api/assignments/' + assignmentId + '/passing-info', callback);
    },
    deleteStartedAssignment: function(assignmentId, callback) {
      this._post('/api/assignments/' + assignmentId + '/delete-started-assignment', {}, callback);
    },

    deleteTest: function(studentId, testId, callback) {
        let data = {
            studentId,
            testId
        };

        this._post('/api/tests/' + testId + '/delete', data, callback);
    },

    resetTest: function(studentId, testId, callback) {
        let data = {
            studentId,
            testId
        };

        this._post('/api/tests/' + testId + '/reset', data, callback);
    },

    regenerateQuiz: function(studentId, quizId, callback) {
        let data = {
            studentId,
            quizId
        };

        this._post('/api/quizzes/' + quizId + '/regenerate', data, callback);
    },

    createDeck: function(studentId, courseId, dueDate, callback) {
        let data = {
            studentId,
            courseId,
            dueDate
        };

        this._post('/api/courses/' + courseId + '/create-flashcards', data, callback);
    },    

    resetDeck: function(studentId, deckId, callback) {
        let data = {
            studentId,
            deckId
        };

        this._post('/api/flashcards/' + deckId + '/reset', data, callback);
    },  

    deleteDeck: function(studentId, deckId, callback) {
        let data = {
            studentId,
            deckId
        };

        this._post('/api/flashcards/' + deckId + '/delete', data, callback);
    },      

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Flashcards

    getCourseFlashcards(courseId, callback) {
        this._get('/api/courses/' + courseId + '/flashcards', callback);
    },

    updateFlashcardPriority(flashcardId, priority, callback) {
        let data = { flashcardId, priority };
        this._post('/api/flashcards/' + flashcardId + '/priority', data, callback);
    },

    updateFlashcardTimeLimit(flashcardId, timeLimit, callback) {
        let data = { flashcardId, timeLimit };
        this._post('/api/flashcards/' + flashcardId + '/time-limit', data, callback);
    },
    
    getDeck: function(deckId, callback) {
        this._get('/api/flashcards/' + deckId, callback);
    },

    submitFlashcardAnswers(deckId, answers, callback) {
        let data = { deckId, answers };
        this._post('/api/flashcards/' + deckId + '/submit-answers', data, callback);
    },

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Tests

    getStudentTest: function(testId, callback) {
        this._get('/api/tests/' + testId, callback);
    },
    initStudentTest: function(testId, startTime, callback) {
        let data = { testId, startTime };
        this._post('/api/tests/' + testId + '/init', data, callback);
    },
    submitTestAnswer: function(testId, questionId, data, callback) {
        this._post('/api/tests/' + testId + '/questions/' + questionId + '/submit-answer', data, callback);
    },
    selectTestQuestion: function(testId, questionId, callback) {
        let data = { testId, questionId };
        this._post('/api/tests/' + testId + '/questions/' + questionId + '/select-question', data, callback);
    },
    submitTestAnswer: function(testId, questionId, data, callback) {
        this._post('/api/tests/' + testId + '/questions/' + questionId + '/submit-answer', data, callback);
    },
    submitTest: function(taskId, testId, events, callback) {
        let data = { taskId, testId, events };
        this._post('/api/tests/' + testId + '/submit', data, callback);
    },
    testEventsProcessed: function(taskId, testId, callback) {
        this._get('/api/tasks/' + taskId + '/tests/' + testId + '/test-events-processed', callback);
    },
    processTestEvents: function(taskId, testId, events, callback) {
        let data = { taskId, testId, events };
        this._post('/api/tasks/' + taskId + '/tests/' + testId + '/process-test-events', data, callback);
    },
    editTest: function(testId, sectionId, callback) {
        this._get('/api/tests/' + testId + '/edit?sectionId=' + sectionId, callback);
    },
    getTestInfo: function(sectionId, callback) {
        this._get('/api/tests/new?sectionId=' + sectionId, callback);   
    },
    fetchActiveTest: function(courseId, callback) {
        this._get('/api/courses/' + courseId + '/active-test', callback);
    },

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Answers
    submitAnswer: function (questionId, data, callback) {
        this._post('/api/questions/' + questionId + '/submit-answer', data, callback);
    },
    submitReviewAnswer: function (questionId, data, callback) {
        this._post('/api/questions/' + questionId + '/submit-review-answer', data, callback);
    },

    submitReferenceAnswer: function (questionId, data, callback) {
        this._post('/api/questions/' + questionId + '/submit-reference-answer', data, callback);
    },

    //submitTestAnswer: function(questionId, data, callback) {
    //    this._post('/api/questions/' + questionId + '/submit-test-answer', data, callback);
    //},
    getStudentAnswers: function (studentId, offset, callback) {
        this._get('/api/students/' + studentId + '/answers?offset=' + offset, callback);
    },
    getStudentClassAnswers: function(studentId, sectionId, offset, callback) {
        this._get('/api/classes/' + sectionId + '/students/' + studentId + '/answers?offset=' + offset, callback);
    },
    getStudentCourseAnswers: function(studentId, courseId, offset, callback) {
        this._get('/api/courses/' + courseId + '/students/' + studentId + '/answers?offset=' + offset, callback);
    },
    getClassActivity: function (sectionId, limit, offset, callback) {
        this._get('/api/classes-activity/' + sectionId + '?offset=' + offset + '&limit=' + limit, callback);
    },
    checkStudentResult(assignmentId, callback) {
        this._get('/api/assignments/' + assignmentId + '/check', callback);
    },

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Sessions
    checkIsAuth(callback) {
        this._get('/api/check-is-auth', callback);
    },
    login(data, callback) {
        this._post('/api/login', data, callback);
    },
    checkDate(data, callback) {
        this._post('/api/tests/check-date/', data, callback);
    },

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Users

    updateAccount(data, callback) {
        this._post('/api/users/update-account', data, callback);
    },

    updateUsername(username, callback) {
        let data = { username };  
        this._post('/api/users/update-username', data, callback);
    },

    updatePassword(data, callback) {
        this._post('/api/users/update-password', data, callback);
    },

    getUser(userId, callback) {
        this._get('/api/users/' + userId, callback);
    },

    getUserInfo(callback) {
        this._get('/api/users/current', callback);
    },

    resetStudentPassword: function(studentId, newPassword, callback) {
        let data = {
            studentId: studentId,
            newPassword: newPassword
        };

        this._post('/api/students/' + studentId + '/reset-password', data, callback);
    },

    changeStatus(userId, callback) {
        this._post('/api/users/' + userId + '/status', null, callback);
    },


    generateMathJax(sageCode, callback) {
        const proxyurl = "https://cors-anywhere.herokuapp.com/";
        this._post(proxyurl + 'http://aleph.sagemath.org/service', { code: 'print latex('+sageCode+')' }, callback);
    },

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Documentation
    requestTranscript(data, callback) {
        this._post('/api/users/request-transcript', data, callback);
    },

    getStudentTranscriptCourses(studentId, callback) {
        this._get(`/api/users/${studentId}/get-student-transcript-courses`, callback);
    },

    requestProgressReportPreview(studentId, callback) {
        this._get(`/api/users/${studentId}/request-progress-report-preview`, callback);
    },
    
    getStudentProgressReportCourses(studentId, callback) {
        this._get(`/api/users/${studentId}/get-student-progress-report-courses`, callback);
    },

    requestActivityLog(data, callback) {
        this._post('/api/users/request-activity-log', data, callback);
    },

    requestActivityLogPreview(studentId, callback) {
        this._get(`/api/users/${studentId}/request-activity-log-preview`, callback);
    },

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Dates
    formatDate(date, callback){
        this._post('/api/format-assignment-date', {date}, callback);
    },

    storeStudentKGGIF(data, callback) {
        this._post(`/api/students/save-gif`, data, callback);
    },

    getStudentKnowledgeGraph: function(studentId, courseId, callback) {
        let url = '/api/students/' + studentId + '/knowledge-graph';
        if (courseId) {
            url += '?courseId=' + courseId;
        }
        this._get(url, callback);
    }, 

    getCourseKnowledgeGraph_NEW: function(courseId, sequenceId, includeFoundationalTopics, callback) {
        this._get(`/api/courses/${courseId}/knowledge-graph-new?${sequenceId ? `sequenceId=${sequenceId}` : ''}${sequenceId && includeFoundationalTopics ? '&' : ''}${includeFoundationalTopics ? `includeFoundationalTopics=${includeFoundationalTopics}` : ''}`, callback);
    }, 

    ////////////////////////////////////////////////////////////////////////////////////////////////////
    // Helper methods
    _get: function (url, callback) {
        Core.get(url, (error, response) => {
            callback(error, response);
        });
    },
    _post: function (url, data, callback) {
        data = data ? data : {};

        Core.post(url, data, (error, response) => {
            if (callback && typeof callback === "function") {
                callback(error, response);
            }
        });
    },
    _join: function(basePath, path) {
        basePathh = basePath.trim();
        path = path.trim();

        let fullPath = basePath;

        if (basePath[basePath.length - 1] !== '/') {
            fullPath += '/';
        }
        if (path[0] === '/' && path.length > 1) {
            fullPath += path.substring(1);
        } else {
            fullPath += path;
        }

        return fullPath;
    }
};

class APISync {
    /////////////////////////////////////////////////////////////////////////////////////////
    // Dashboard

    /*
    static async getSchool(schoolId) {
        return new Promise((resolve, reject) => {
            API.getSchool(schoolId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });        
        }); 
    }

    static async addSchool(school) {
        return new Promise((resolve, reject) => {
            API.addSchool(school, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async updateSchool(school) {
        return new Promise((resolve, reject) => {
            API.updateSchool(school, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async deleteSchool(schoolId) {
        return new Promise((resolve, reject) => {
            API.deleteSchool(schoolId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }
    */

    ///////////////////////////////////////////////////////////////////////////////////////////////////

    static async postTroubleshooting(taskId, entries) {
        return new Promise((resolve, reject) => {
            API.postTroubleshooting(taskId, entries, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async createQuestionGroup(data) {
        return new Promise((resolve, reject) => {
            API.createQuestionGroup(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }
    
    static async updateQuestionGroup(data) {
        return new Promise((resolve, reject) => {
            API.updateQuestionGroup(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }    

    static async updateQuestionGroupTarget(questionGroupId, target, modelType) {
        return new Promise((resolve, reject) => {
            API.updateQuestionGroupTarget(questionGroupId, target, modelType, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }    

    static async transposeQuestionGroups(group1Id, group2Id) {
        return new Promise((resolve, reject) => {
            API.transposeQuestionGroups(group1Id, group2Id, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async removeQuestionGroup(groupId) {
        return new Promise((resolve, reject) => {
            API.removeQuestionGroup(groupId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getUserInfo() {
        return new Promise((resolve, reject) => {
            API.getUserInfo((error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.user);
                }
            });        
        }); 
    }

    static async getTopicQuestionsMetaData(topicId) {
        return new Promise((resolve, reject) => {
            API.getTopicQuestionsMetaData(topicId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        }); 
    }

    static async checkAssignedQuestionsCount(topicId) {
        return new Promise((resolve, reject) => {
            API.checkAssignedQuestionsCount(topicId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.result);
                }
            });
        }); 
    }           

    static async updateQuestionDifficulty(questionId, difficulty) {
        return new Promise((resolve, reject) => {
            API.updateQuestionDifficulty(questionId, difficulty, (error, response) => {
                if (error) {
                    resolve(false);
                } else {
                    resolve(true);
                }
            });
        });
    }

    static async updateQuestionType(questionId, questionType) {
        return new Promise((resolve, reject) => {
            API.updateQuestionType(questionId, questionType, (error, response) => {
                if (error) {
                    resolve(false);
                } else {
                    resolve(true);
                }
            });
        });
    }

    static async updateQuestion(data) {
        return new Promise((resolve, reject) => {
            API.updateQuestion(data, (error, response) => {
                if (error) {
                    resolve(false);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async createQuestion(data) {
        return new Promise((resolve, reject) => {
            API.createQuestion(data, (error, response) => {
                if (error) {
                    resolve(false);
                } else {
                    resolve(response.data);
                }
            });
        });
    }

    static async moveQuestionToGroup(questionId, exampleId, groupId) {
        return new Promise((resolve, reject) => {
            API.moveQuestionToGroup(questionId, exampleId, groupId, (error, response) => {
                if (error) {
                    resolve(false);
                } else {
                    resolve(true);
                }
            });
        });
    }

    /*
    static async updateQuestion(data) {
        return new Promise((resolve, reject) => {
            API.updateQuestion(data), (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }
    */

    static async getLesson(topicId) {
        return new Promise((resolve, reject) => {
            API.getLesson(topicId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.lesson);
                }
            });
        });
    }   

    static async getExample(exampleId) {
        return new Promise((resolve, reject) => {
            API.getExample(exampleId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.example);
                }
            });
        });
    }   

    static async getGroupQuestions(groupId) {
        return new Promise((resolve, reject) => {
            API.getGroupQuestions(groupId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.questions);
                }
            });
        });
    }   

    static async getGroupQuestionsBasic(groupId) {
        return new Promise((resolve, reject) => {
            API.getGroupQuestionsBasic(groupId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.questions);
                }
            });
        });
    }   
    
    static async getUncategorizedQuestions(topicId) {
        return new Promise((resolve, reject) => {
            API.getUncategorizedQuestions(topicId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.questions);
                }
            });
        });
    }  

    static async getQuestion(questionId) {
        return new Promise((resolve, reject) => {
            API.getQuestion(questionId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.data);
                }
            });
        });
    }    

    static async getQuestionComplete(questionId) {
        return new Promise((resolve, reject) => {
            API.getQuestionComplete(questionId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.question);
                }
            });
        });
    }   

    static async getQuestionStatus(questionId) {
        return new Promise((resolve, reject) => {        
            API.getQuestionStatus(questionId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.status);
                }
            });
        });
    }

    static async getQuestionStats(questionId) {
        return new Promise((resolve, reject) => {        
            API.getQuestionStats(questionId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.data);
                }
            });
        });
    }

    static async submitQuestion(questionId) {
        return new Promise((resolve, reject) => {
            API.submitQuestion(questionId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.data);
                }
            });
        });
    }    

    static async acceptQuestion(questionId) {
        return new Promise((resolve, reject) => {
            API.acceptQuestion(questionId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.event);
                }
            });
        });
    }       
    
    static async acceptQuestions(questionIds) {
        return new Promise((resolve, reject) => {
            API.acceptQuestions(questionIds, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.events);
                }
            });
        });
    }       

    static async deleteQuestion(questionId) {
        return new Promise((resolve, reject) => {
            API.deleteQuestion(questionId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async restoreQuestion(questionId) {
        return new Promise((resolve, reject) => {
            API.restoreQuestion(questionId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });                
    }

    static async resolveQuestionFlags(questionId) {
        return new Promise((resolve, reject) => {
            API.resolveQuestionFlags(questionId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.data);
                }
            });
        });                
    }

    static async recheckQuestion(questionId) {
        return new Promise((resolve, reject) => {
            API.recheckQuestion(questionId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });                
    }

    static async generateGraphic(questionId, fieldName, tex, graphicsVersion) {
        return new Promise((resolve, reject) => {
            API.generateGraphic(questionId, fieldName, tex, graphicsVersion, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.data);
                }
            });
        });   
    }

    static async getNextAssignmentQuestion(assignmentId) {
        return new Promise((resolve, reject) => {
            API.getNextAssignmentQuestion(assignmentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getNextReviewQuestion(taskId) {
        return new Promise((resolve, reject) => {
            API.getNextReviewQuestion(taskId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getTaskLessonState(taskId, topicId) {
        return new Promise((resolve, reject) => {
            API.getTaskLessonState(taskId, topicId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getTaskReviewState(taskId, topicId) {
        return new Promise((resolve, reject) => {
            API.getTaskReviewState(taskId, topicId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getTaskDrillState(taskId, topicId) {
        return new Promise((resolve, reject) => {
            API.getTaskDrillState(taskId, topicId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }    

    static async getTaskMultistepState(taskId, multistepId) {
        return new Promise((resolve, reject) => {
            API.getTaskMultistepState(taskId, multistepId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }  

    static async selectLessonStep(taskId, topicId, lessonStructure, stepNumber, questionId) {
        return new Promise((resolve, reject) => {
            API.selectLessonStep(taskId, topicId, lessonStructure, stepNumber, questionId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }  

    static async submitLessonAnswer(taskId, topicId, data) {
        return new Promise((resolve, reject) => {
            API.submitLessonAnswer(taskId, topicId, data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }    
    static async submitAnswer(questionId, data) {
        return new Promise((resolve, reject) => {
            API.submitAnswer(questionId, data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async submitReviewAnswer(questionId, data) {
        return new Promise((resolve, reject) => {
            API.submitReviewAnswer(questionId, data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async submitReferenceAnswer(questionId, data) {
        return new Promise((resolve, reject) => {
            API.submitReferenceAnswer(questionId, data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async submitDiagnosticAnswer(diagnosticId, data) {
        return new Promise((resolve, reject) => {
            API.submitDiagnosticAnswer(diagnosticId, data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 
 
    static async getTaskAnswers(taskId) {
        return new Promise((resolve, reject) => {
            API.getTaskAnswers(taskId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getNewTasks() {
        return new Promise((resolve, reject) => {
            API.getNewTasks((error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getPreviousTasks(date, minumum = 25) {
        return new Promise((resolve, reject) => {
            API.getPreviousTasks(date, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            }, minumum);
        });
    }

    static async fetchActiveTest(courseId) {
        return new Promise((resolve, reject) => {
            API.fetchActiveTest(courseId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 
        
    static async getCourseKnowledgeGraphSVG(courseId) {
        return new Promise((resolve, reject) => {
            API.getCourseKnowledgeGraphSVG(courseId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.data);
                }
            });
        });
    }

    static async getClassPriorityTopics(classId) {
        return new Promise((resolve, reject) => {
            API.getClassPriorityTopics(classId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getClassPriorityTopicsByCourse(sectionId, courseIds) {
        return new Promise((resolve, reject) => {
            API.getClassPriorityTopicsByCourse(sectionId, courseIds, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.courses);
                }
            });
        });
    }

    static async getStudentPriorityTopics(studentId) {
        return new Promise((resolve, reject) => {
            API.getStudentPriorityTopics(studentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }    

    static async addClassPriorityTopic(sectionId, topicId) {
        return new Promise((resolve, reject) => {
            API.addClassPriorityTopic(sectionId, topicId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async removeClassPriorityTopic(sectionId, topicId) {
        return new Promise((resolve, reject) => {
            API.removeClassPriorityTopic(sectionId, topicId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }    

    static async updateClassPriorityTopics(classId, priorityTopicIds) {
        return new Promise((resolve, reject) => {
            API.updateClassPriorityTopics(classId, priorityTopicIds, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async updateStudentPriorityTopics(studentId, priorityTopicIds) {
        return new Promise((resolve, reject) => {
            API.updateStudentPriorityTopics(studentId, priorityTopicIds, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 


    static async createMultistepType(courseId, name, description) {
        return new Promise((resolve, reject) => {
            API.createMultistepType(courseId, name, description, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async updateMultistepType(multistepTypeId, name, description) {
        return new Promise((resolve, reject) => {
            API.updateMultistepType(multistepTypeId, name, description, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }     

    static async updateMultistepTypeLive(multistepTypeId, live) {
        return new Promise((resolve, reject) => {
            API.updateMultistepTypeLive(multistepTypeId, live, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }     

    static async deleteMultistepType(multistepTypeId) {
        return new Promise((resolve, reject) => {
            API.deleteMultistepType(multistepTypeId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }       

    static async getMultistepTypes(courseId) {
        return new Promise((resolve, reject) => {
            API.getMultistepTypes(courseId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getMultistepType(multistepTypeId) {
        return new Promise((resolve, reject) => {
            API.getMultistepType(multistepTypeId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getMultistep(multistepId, process) {
        return new Promise((resolve, reject) => {
            API.getMultistep(multistepId, process, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.multistep);
                }
            });
        });
    }

    static async getMultistepSteps(multistepId) {
        return new Promise((resolve, reject) => {
            API.getMultistepSteps(multistepId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.steps);
                }
            });
        });
    }

    static async transposeMultistepSteps(multistepId, projectStepId1, projectStepId2) {
        return new Promise((resolve, reject) => {
            API.transposeMultistepSteps(multistepId, projectStepId1, projectStepId2, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async insertMultistepTutorialStep(multistepId, stepNumber, title, content, graphics) {
        return new Promise((resolve, reject) => {
            API.insertMultistepTutorialStep(multistepId, stepNumber, title, content, graphics, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.step);
                }
            });
        });
    }

    static async getMultistepTutorial(multistepId, tutorialId) {
        return new Promise((resolve, reject) => {
            API.getMultistepTutorial(multistepId, tutorialId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.tutorial);
                }
            });
        });
    }

    static async updateMultistepTutorial(multistepId, tutorialId, content, graphics) {
        return new Promise((resolve, reject) => {
            API.updateMultistepTutorial(multistepId, tutorialId, content, graphics, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.html);
                }
            });
        });
    }

    static async updateMultistepTutorialTitle(multistepId, tutorialId, title) {
        return new Promise((resolve, reject) => {
            API.updateMultistepTutorialTitle(multistepId, tutorialId, title, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async deleteMultistepTutorialStep(multistepId, stepNumber) {
        return new Promise((resolve, reject) => {
            API.deleteMultistepTutorialStep(multistepId, stepNumber, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async createMultistep(multistepTypeId, text, graphics) {
        return new Promise((resolve, reject) => {
            API.createMultistep(multistepTypeId, text, graphics, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.multistep);
                }
            });
        });
    } 

    static async updateMultistep(multistepId, text, graphics) {
        return new Promise((resolve, reject) => {
            API.updateMultistep(multistepId, text, graphics, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.multistep);
                }
            });
        });
    }      

    static async deleteMultistep(multistepId) {
        return new Promise((resolve, reject) => {
            API.deleteMultistep(multistepId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }     

    static async cloneMultistep(multistepId) {
        return new Promise((resolve, reject) => {
            API.cloneMultistep(multistepId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.multistep);
                }
            });
        });
    }    

    static async transposeMultistepQuestions(multistepId, question1Id, question2Id) {
        return new Promise((resolve, reject) => {
            API.transposeMultistepQuestions(multistepId, question1Id, question2Id, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }  

    static async submitMultistep(multistepId) {
        return new Promise((resolve, reject) => {
            API.submitMultistep(multistepId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.events);
                }
            });
        });
    }    

    static async unsubmitMultistep(multistepId) {
        return new Promise((resolve, reject) => {
            API.unsubmitMultistep(multistepId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.events);
                }
            });
        });
    } 
    
    static async acceptMultistep(multistepId) {
        return new Promise((resolve, reject) => {
            API.acceptMultistep(multistepId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.events);
                }
            });
        });
    }  

    static async unacceptMultistep(multistepId) {
        return new Promise((resolve, reject) => {
            API.unacceptMultistep(multistepId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.events);
                }
            });
        });
    }      

    static async deleteMultistepQuestion(multistepId, questionId, stepNumber) {
        return new Promise((resolve, reject) => {
            API.deleteMultistepQuestion(multistepId, questionId, stepNumber, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }         

    static async getTopicExamples(topicId) {
        return new Promise((resolve, reject) => {
            API.getTopicExamples(topicId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.examples);
                }
            });
        });
    }

    static async updateMultistepQuestionKP(multistepTypeId, stepNumber, topicId, exampleId) {
        return new Promise((resolve, reject) => {
            API.updateMultistepQuestionKP(multistepTypeId, stepNumber, topicId, exampleId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }     
    
    static async updateMultistepQuestionDifficulty(multistepTypeId, stepNumber, difficulty) {
        return new Promise((resolve, reject) => {
            API.updateMultistepQuestionDifficulty(multistepTypeId, stepNumber, difficulty, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }     

    static async selectTaskQuestion(taskId, questionId) {
        return new Promise((resolve, reject) => {
            API.selectTaskQuestion(taskId, questionId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }    

    static async submitMultistepAnswer(taskId, multistepId, data) {
        return new Promise((resolve, reject) => {
            API.submitMultistepAnswer(taskId, multistepId, data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }    

    static async getDiagnosticAnalysis(diagnosticId, taskId) {
        return new Promise((resolve, reject) => {
            API.getDiagnosticAnalysis(diagnosticId, taskId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async updateAccount(data) {
        return new Promise((resolve, reject) => {
            API.updateAccount(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }   

    static async updateUsername(username) {
        return new Promise((resolve, reject) => {
            API.updateUsername(username, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async updatePassword(data) {
        return new Promise((resolve, reject) => {
            API.updatePassword(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async confirmPopupNotification(id) {
        return new Promise((resolve, reject) => {
            API.confirmPopupNotification(id, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async signUp(data) {
        return new Promise((resolve, reject) => {
            API.signUp(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async getIncompleteSubscriptions() {
        return new Promise((resolve, reject) => {
            API.getIncompleteSubscriptions((error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getRequireActionSubscriptions() {
        return new Promise((resolve, reject) => {
            API.getRequireActionSubscriptions((error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getSubscription(subscriptionId) {
        return new Promise((resolve, reject) => {
            API.getSubscription(subscriptionId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async finalizeSignUp() {
        return new Promise((resolve, reject) => {
            API.finalizeSignUp((error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async finalizeAddStudentAccount(data) {
        return new Promise((resolve, reject) => {
            API.finalizeAddStudentAccount(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }     

    static async setSubscriptionPaymentError(paymentError) {
        return new Promise((resolve, reject) => {
            API.setSubscriptionPaymentError(paymentError, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async reportSubscriptionConfirmationResults(results) {
        return new Promise((resolve, reject) => {
            API.reportSubscriptionConfirmationResults(results, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async cleanUpAfterFailedPayment() {
        return new Promise((resolve, reject) => {
            API.cleanUpAfterFailedPayment((error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getStudent(studentId) {
        return new Promise((resolve, reject) => {
            API.getStudent(studentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getStudentXPGoals(studentId) {
        return new Promise((resolve, reject) => {
            API.getStudentXPGoals(studentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getStudentCourse(studentId, courseId) {
        return new Promise((resolve, reject) => {
            API.getStudentCourse(studentId, courseId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.studentCourse);
                }
            });
        });
    }

    static async updateStudentCourse(studentId, data) {
        return new Promise((resolve, reject) => {
            API.updateStudentCourse(studentId, data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getActiveStudentCourse(studentId) {
        return new Promise((resolve, reject) => {
            API.getActiveStudentCourse(studentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async resetStudentCourse(studentId, courseId) {
        return new Promise((resolve, reject) => {
            API.resetStudentCourse(studentId, courseId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async resetKnowledgeProfile(studentId) {
        return new Promise((resolve, reject) => {
            API.resetKnowledgeProfile(studentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async assignDiagnostic(studentId, courseId) {
        return new Promise((resolve, reject) => {
            API.assignDiagnostic(studentId, courseId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async updateStudentXPGoals(studentId, data) {
        return new Promise((resolve, reject) => {
            API.updateStudentXPGoals(studentId, data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async getStudentAccommodations(studentId) {
        return new Promise((resolve, reject) => {
            API.getStudentAccommodations(studentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async updateStudentAccommodations(studentId, data) {
        return new Promise((resolve, reject) => {
            API.updateStudentAccommodations(studentId, data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }     

    static async sendClassInvitations(classId, emails) {
        return new Promise((resolve, reject) => {
            API.sendClassInvitations(classId, emails, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async initiatePasswordReset(email) {
        return new Promise((resolve, reject) => {
            API.initializePasswordReset(email, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }   

    static async reconfigureAccount(data) {
        return new Promise((resolve, reject) => {
            API.reconfigureAccount(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async saveStudentAccount(data) {
        return new Promise((resolve, reject) => {
            API.saveStudentAccount(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async addStudentAccount(data) {
        return new Promise((resolve, reject) => {
            API.addStudentAccount(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async reactivateStudentAccount(studentId, subscription) {
        return new Promise((resolve, reject) => {
            API.reactivateStudentAccount(studentId, subscription, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async addGuardianAccount(data) {
        return new Promise((resolve, reject) => {
            API.addGuardianAccount(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }    

    static async updateAccountAccess(studentId, guardianId, access) {
        return new Promise((resolve, reject) => {
            API.updateAccountAccess(studentId, guardianId, access, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }  

    static async removeAccountAccess(studentId, guardianId) {
        return new Promise((resolve, reject) => {
            API.removeAccountAccess(studentId, guardianId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }    

    static async updatePaymentMethod(token) {
        return new Promise((resolve, reject) => {
            API.updatePaymentMethod(token, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async upgradeSubscription(studentId) {
        return new Promise((resolve, reject) => {
            API.upgradeSubscription(studentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async upgradeSubscriptionToLifetime(studentId) {
        return new Promise((resolve, reject) => {
            API.upgradeSubscriptionToLifetime(studentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async finalizeUpgradeSubscription(studentId) {
        return new Promise((resolve, reject) => {
            API.finalizeUpgradeSubscription(studentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async pauseSubscription(studentId, resumeOn) {
        return new Promise((resolve, reject) => {
            API.pauseSubscription(studentId, resumeOn, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async cancelSubscription(studentId, reason) {
        return new Promise((resolve, reject) => {
            API.cancelSubscription(studentId, reason, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async switchUserAccount(userIdentifier) {
        return new Promise((resolve, reject) => {
            API.switchUserAccount(userIdentifier, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async isEmailAvailable(email) {
        return new Promise((resolve, reject) => {
            API.isEmailAvailable(email, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async isStudentAccountEmailAvailable(studentAccountId, email) {
        return new Promise((resolve, reject) => {
            API.isStudentAccountEmailAvailable(studentAccountId, email, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }        

    static async getTutorial(tutorialId) {
        return new Promise((resolve, reject) => {
            API.getTutorial(tutorialId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.data);
                }
            });
        });
    }

    static async updateTutorial(tutorialId, content, graphics) {
        return new Promise((resolve, reject) => {
            API.updateTutorial(tutorialId, content, graphics, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }    

    static async updateTutorialTitle(tutorialId, title) {
        return new Promise((resolve, reject) => {
            API.updateTutorialTitle(tutorialId, title, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }  

    static async getExample(exampleId) {
        return new Promise((resolve, reject) => {
            API.getExample(exampleId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.data);
                }
            });
        });
    }

    static async updateExample(exampleId, question, explanation, graphics) {
        return new Promise((resolve, reject) => {
            API.updateExample(exampleId, question, explanation, graphics, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }   

    static async updateExampleTitle(exampleId, title) {
        return new Promise((resolve, reject) => {
            API.updateExampleTitle(exampleId, title, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }  

    static async submitQuestionComment(questionId, content) {
        return new Promise((resolve, reject) => {
            API.submitQuestionComment(questionId, content, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async deleteComment(commentId) {
        return new Promise((resolve, reject) => {
            API.deleteComment(commentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }  

    static async archiveComment(commentId) {
        return new Promise((resolve, reject) => {
            API.archiveComment(commentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }  

    static async getStudentTest(testId) {
        return new Promise((resolve, reject) => {
            API.getStudentTest(testId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.test);
                }
            });
        });
    }

    static async initStudentTest(testId, startTime) {
        return new Promise((resolve, reject) => {
            API.initStudentTest(testId, startTime, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.data);
                }
            });
        });
    }

    static async testEventsProcessed(taskId, testId) {
        return new Promise((resolve, reject) => {
            API.testEventsProcessed(taskId, testId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.result);
                }
            });
        });
    }

    static async processTestEvents(taskId, testId, events) {
        return new Promise((resolve, reject) => {
            API.processTestEvents(taskId, testId, events, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getLesson(topicId) {
        return new Promise((resolve, reject) => {
            API.getLesson(topicId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.lesson);
                }
            });
        });
    }

    static async getReferenceLesson(topicId) {
        return new Promise((resolve, reject) => {
            API.getReferenceLesson(topicId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response.lesson);
                }
            });
        });
    }

    static async getNextDiagnosticQuestion(diagnosticId, taskId, retry) {
        return new Promise((resolve, reject) => {
            API.getNextDiagnosticQuestion(diagnosticId, taskId, retry, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async submitRequestProfile(data) {
        return new Promise((resolve, reject) => {
            API.submitRequestProfile(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }  

    static async postTaskEvents(taskId, data) {
        return new Promise((resolve, reject) => {
            API.postTaskEvents(taskId, data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }  
  
    static async requestTranscript(data) {
        return new Promise((resolve, reject) => {
            API.requestTranscript(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }
  
    static async getStudentTranscriptCourses(studentId) {
        return new Promise((resolve, reject) => {
            API.getStudentTranscriptCourses(studentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getStudentProgressReportCourses(studentId) {
        return new Promise((resolve, reject) => {
            API.getStudentProgressReportCourses(studentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async requestActivityLog(data) {
        return new Promise((resolve, reject) => {
            API.requestActivityLog(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async requestActivityLogPreview() {
        return new Promise((resolve, reject) => {
            API.requestActivityLog((error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }



    static async createDocument(document) {
        return new Promise((resolve, reject) => {
            API.createDocument(document, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }  

    static async getDocument(documentId) {
        return new Promise((resolve, reject) => {
            API.getDocument(documentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async updateDocument(documentId, document) {
        return new Promise((resolve, reject) => {
            API.updateDocument(documentId, document, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }  

    static async updateDocumentContent(documentId, document) {
        return new Promise((resolve, reject) => {
            API.updateDocumentContent(documentId, document, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async publishDocument(documentId) {
        return new Promise((resolve, reject) => {
            API.publishDocument(documentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }  

    static async unpublishDocument(documentId) {
        return new Promise((resolve, reject) => {
            API.unpublishDocument(documentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }  

    static async publishDocumentLastRevision(documentId) {
        return new Promise((resolve, reject) => {
            API.publishDocumentLastRevision(documentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }  

    static async discardDocumentLastRevision(documentId) {
        return new Promise((resolve, reject) => {
            API.discardDocumentLastRevision(documentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }  

    static async deleteDocument(documentId) {
        return new Promise((resolve, reject) => {
            API.deleteDocument(documentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }  

    static async getCollections() {
        return new Promise((resolve, reject) => {
            API.getCollections((error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async createCollection(collection) {
        return new Promise((resolve, reject) => {
            API.createCollection(collection, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }  

    static async updateCollection(collectionId, collection) {
        return new Promise((resolve, reject) => {
            API.updateCollection(collectionId, collection, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }  

    static async saveCollection(collection) {
        if (collection.id) {
            return await this.updateCollection(collection.id, collection);
        } else {
            return await this.createCollection(collection);
        }
    }  

    static async saveObject(objectType, data) {
        return new Promise((resolve, reject) => {
            API.saveObject(objectType, data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }  

    static async acceptVersionUpgrade(studentId, courseId) {
        return new Promise((resolve, reject) => {
            API.acceptVersionUpgrade(studentId, courseId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async declineVersionUpgrade(studentId, courseId) {
        return new Promise((resolve, reject) => {
            API.declineVersionUpgrade(studentId, courseId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }  

    static async acknowledgeVersionUpgrade(studentId, courseId) {
        return new Promise((resolve, reject) => {
            API.acknowledgeVersionUpgrade(studentId, courseId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }  

    static async getCoursesByCategory(locale) {
        return new Promise((resolve, reject) => {
            API.getCoursesByCategory(locale, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async getCoursesByCategoryWithDevelopment(locale) {
        return new Promise((resolve, reject) => {
            API.getCoursesByCategoryWithDevelopment(locale, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async getCourseContent(courseId) {
        return new Promise((resolve, reject) => {
            API.getCourseContent(courseId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async getStudentCourseStatus(studentId, courseId) {
        return new Promise((resolve, reject) => {
            API.getStudentCourseStatus(studentId, courseId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async getStudentCourseContent(studentId, courseId) {
        return new Promise((resolve, reject) => {
            API.getStudentCourseContent(studentId, courseId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async getNewVersionOfCourse(courseId) {
        return new Promise((resolve, reject) => {
            API.getNewVersionOfCourse(courseId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async getIncompleteDiagnosticTask(studentId, courseId) {
        return new Promise((resolve, reject) => {
            API.getIncompleteDiagnosticTask(studentId, courseId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async getIncompleteTasks(studentId, courseId) {
        return new Promise((resolve, reject) => {
            API.getIncompleteTasks(studentId, courseId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async applyPromoCode(promoCode) {
        return new Promise((resolve, reject) => {
            API.applyPromoCode(promoCode, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }     

    static async getPaymentTaxAndTotal(data) {
        return new Promise((resolve, reject) => {
            API.getPaymentTaxAndTotal(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }     

    static async getCodeFiles() {
        return new Promise((resolve, reject) => {
            API.getCodeFiles((error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async getCodeFile(name) {
        return new Promise((resolve, reject) => {
            API.getCodeFile(name, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async saveCode(name, code) {
        return new Promise((resolve, reject) => {
            API.saveCodeFile(name, code, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async getUser(userId) {
        return new Promise((resolve, reject) => {
            API.getUser(userId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async createCharterStudentAccount(data) {
        return new Promise((resolve, reject) => {
            API.createCharterStudentAccount(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async updateCharterStudentAccount(studentId, data) {
        return new Promise((resolve, reject) => {
            API.updateCharterStudentAccount(studentId, data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }    

    static async transferCharterStudentAccount(studentId, data) {
        return new Promise((resolve, reject) => {
            API.transferCharterStudentAccount(studentId, data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }      

    static async mergeStudentGuardianAccounts(studentId, guardianId) {
        return new Promise((resolve, reject) => {
            API.mergeStudentGuardianAccounts(studentId, guardianId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async splitAdultStudentAccount(data) {
        return new Promise((resolve, reject) => {
            API.splitAdultStudentAccount(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async cancelStudentAccount(studentId, cancelSubscription, refund, cancelReason, deactivateImmediately) {
        return new Promise((resolve, reject) => {
            API.cancelStudentAccount(studentId, cancelSubscription, refund, cancelReason, deactivateImmediately, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async deactivateAccount(studentId) {
        return new Promise((resolve, reject) => {
            API.deactivateAccount(studentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getSchoolInstructors() {
        return new Promise((resolve, reject) => {
            API.getSchoolInstructors((error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async moveStudentToClass(studentId, classId) {
        return new Promise((resolve, reject) => {
            API.moveStudentToClass(studentId, classId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getSchoolClasses() {
        return new Promise((resolve, reject) => {
            API.getSchoolClasses((error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getClass(classId) {
        return new Promise((resolve, reject) => {
            API.getClass(classId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getClassCourses(classId) {
        return new Promise((resolve, reject) => {
            API.getClassCourses(classId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getStudentCurrentCourse(studentId) {
        return new Promise((resolve, reject) => {
            API.getStudentCurrentCourse(studentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async createSchool(data) {
        return new Promise((resolve, reject) => {
            API.createSchool(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async updateSchool(schoolId, data) {
        return new Promise((resolve, reject) => {
            API.updateSchool(schoolId, data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async createOrganization(data) {
        return new Promise((resolve, reject) => {
            API.createOrganization(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getStripeProducts() {
        return new Promise((resolve, reject) => {
            API.getStripeProducts((error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async updateOrganization(organizationId, data) {
        return new Promise((resolve, reject) => {
            API.updateOrganization(organizationId, data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getOrganization(organizationId) {
        return new Promise((resolve, reject) => {
            API.getOrganization(organizationId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getOrganizations() {
        return new Promise((resolve, reject) => {
            API.getOrganizations((error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getOrganizationSchools(organizationId) {
        return new Promise((resolve, reject) => {
            API.getOrganizationSchools(organizationId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async activateOrganizationAccount(organizationId, data) {
        return new Promise((resolve, reject) => {
            API.activateOrganizationAccount(organizationId, data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async cancelOrganizationAccount(organizationId) {
        return new Promise((resolve, reject) => {
            API.cancelOrganizationAccount(organizationId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async searchOrganizations(lookup) {
        return new Promise((resolve, reject) => {
            API.searchOrganizations(lookup, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async importStudents(schoolId, data) {
        return new Promise((resolve, reject) => {
            API.importStudents(schoolId, data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }   

    static async cancelSchoolAccount(schoolId) {
        return new Promise((resolve, reject) => {
            API.cancelSchoolAccount(schoolId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }     

    static async reactivateSchoolAccount(schoolId) {
        return new Promise((resolve, reject) => {
            API.reactivateSchoolAccount(schoolId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async createClass(data) {
        return new Promise((resolve, reject) => {
            API.createClass(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async updateClass(classId, data) {
        return new Promise((resolve, reject) => {
            API.updateClass(classId, data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async createSchoolStudentAccount(data) {
        return new Promise((resolve, reject) => {
            API.createSchoolStudentAccount(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async deactivateSchoolStudentAccount(studentId) {
        return new Promise((resolve, reject) => {
            API.deactivateSchoolStudentAccount(studentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async reactivateSchoolStudentAccount(studentId) {
        return new Promise((resolve, reject) => {
            API.reactivateSchoolStudentAccount(studentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }    

    static async getSchoolUserAccount(userId) {
        return new Promise((resolve, reject) => {
            API.getSchoolUserAccount(userId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async createSchoolUserAccount(data) {
        return new Promise((resolve, reject) => {
            API.createSchoolUserAccount(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async updateSchoolUserAccount(data) {
        return new Promise((resolve, reject) => {
            API.updateSchoolUserAccount(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async deactivateSchoolUserAccount(userId) {
        return new Promise((resolve, reject) => {
            API.deactivateSchoolUserAccount(userId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async reactivateSchoolUserAccount(userId) {
        return new Promise((resolve, reject) => {
            API.reactivateSchoolUserAccount(userId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }  

    static async deleteUserInfo(userId) {
        return new Promise((resolve, reject) => {
            API.deleteUserInfo(userId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async generateUserPassword(userId) {
        return new Promise((resolve, reject) => {
            API.generateUserPassword(userId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async deleteTask(taskId) {
        return new Promise((resolve, reject) => {
            API.deleteTask(taskId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async transferTask(taskId, destinationStudentId) {
        return new Promise((resolve, reject) => {
            API.transferTask(taskId, destinationStudentId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getTaskInfo(taskId) {
        return new Promise((resolve, reject) => {
            API.getTaskInfo(taskId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async updateUserCategories(userId, categories) {
        return new Promise((resolve, reject) => {
            API.updateUserCategories(userId, categories, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async exportContext(topicId, data) {
        return new Promise((resolve, reject) => {
            API.exportContext(topicId, data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async exportLesson(topicId, includeImagesAndTables) {
        return new Promise((resolve, reject) => {
            API.exportLesson(topicId, includeImagesAndTables, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async importQuestions(topicId, data) {
        return new Promise((resolve, reject) => {
            API.importQuestions(topicId, data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async importProject(courseId, data) {
        return new Promise((resolve, reject) => {
            API.importProject(courseId, data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });  
    } 

    static async importLesson(topicId, data) {
        return new Promise((resolve, reject) => {
            API.importLesson(topicId, data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async importLessons(data) {
        return new Promise((resolve, reject) => {
            API.importLessons(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async deleteLesson(topicId) {
        return new Promise((resolve, reject) => {
            API.deleteLesson(topicId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async submitLesson(lessonId) {
        return new Promise((resolve, reject) => {
            API.submitLesson(lessonId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async acceptLesson(lessonId, forceReason = null) {
        return new Promise((resolve, reject) => {
            API.acceptLesson(lessonId, forceReason, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async submitTopic(topicId, lessonId) {
        return new Promise((resolve, reject) => {
            API.submitTopic(topicId, lessonId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async acceptTopic(topicId, forceReason = null) {
        return new Promise((resolve, reject) => {
            API.acceptTopic(topicId, forceReason, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }    

    static async submitTopicTutorialsAndExamples(topicId) {
        return new Promise((resolve, reject) => {
            API.submitTopicTutorialsAndExamples(topicId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }    

    static async submitTutorial(tutorialId) {
        return new Promise((resolve, reject) => {
            API.submitTutorial(tutorialId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }   

    static async acceptTutorial(tutorialId, forceReason = null) {
        return new Promise((resolve, reject) => {
            API.acceptTutorial(tutorialId, forceReason, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }      

    static async submitExample(exampleId) {
        return new Promise((resolve, reject) => {
            API.submitExample(exampleId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }       
    
    static async acceptExample(exampleId, forceReason = null) {
        return new Promise((resolve, reject) => {
            API.acceptExample(exampleId, forceReason, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    } 

    static async getTopicMetaData(topicId) {
        return new Promise((resolve, reject) => {
            API.getTopicMetaData(topicId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async searchExamples(searchText, formats, offset = 0) {
        return new Promise((resolve, reject) => {
            API.searchExamples(searchText, formats, offset, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }    

    static async searchGraphics(searchText, topicId = null) {
        return new Promise((resolve, reject) => {
            API.searchGraphics(searchText, topicId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getExampleGraphics(topicId, exampleId) {
        return new Promise((resolve, reject) => {
            API.getExampleGraphics(topicId, exampleId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getTutorialGraphics(topicId, tutorialId) {
        return new Promise((resolve, reject) => {
            API.getTutorialGraphics(topicId, tutorialId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getExemplars(exampleId, formats) {
        return new Promise((resolve, reject) => {
            API.getExemplars(exampleId, formats, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async createAccountTransferRequest(data) {
        return new Promise((resolve, reject) => {
            API.createAccountTransferRequest(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }     

    static async updateTimeZone(timeZone) {
        return new Promise((resolve, reject) => {
            API.updateTimeZone(timeZone, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }  

    static async getLessonStepTutorial(lessonId, tutorialId) {
        return new Promise((resolve, reject) => {
            API.getLessonStepTutorial(lessonId, tutorialId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }
    
    static async getStudentKnowledgeGraph(studentId, courseId = null) {
        return new Promise((resolve, reject) => {
            API.getStudentKnowledgeGraph(studentId, courseId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getCourseKnowledgeGraph_NEW(courseId, sequenceId = null, includeFoundationalTopics = null) {
        return new Promise((resolve, reject) => {
            API.getCourseKnowledgeGraph_NEW(courseId, sequenceId, includeFoundationalTopics, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async storeStudentKGGIF(data) {
        return new Promise((resolve, reject) => {
            API.storeStudentKGGIF(data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }    

    static async getLessonStepExample(lessonId, exampleId) {
        return new Promise((resolve, reject) => {
            API.getLessonStepExample(lessonId, exampleId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }       

    static async insertLessonStepTutorial(topicId, lessonId, stepNumber, content, graphics) {
        return new Promise((resolve, reject) => {
            API.insertLessonStepTutorial(topicId, lessonId, stepNumber, content, graphics, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }      

    static async insertLessonStepExample(topicId, lessonId, stepNumber, question, explanation, graphics) {
        return new Promise((resolve, reject) => {
            API.insertLessonStepExample(topicId, lessonId, stepNumber, question, explanation, graphics, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }          

    // API.updateLessonStepTutorial(this.lessonId, tutorialId, content, graphics
    static async updateLessonStepTutorial(lessonId, tutorialId, content, graphics) {
        return new Promise((resolve, reject) => {
            API.updateLessonStepTutorial(lessonId, tutorialId, content, graphics, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }       
    
    static async updateLessonStepExample(lessonId, exampleId, question, explanation, graphics) {
        return new Promise((resolve, reject) => {
            API.updateLessonStepExample(lessonId, exampleId, question, explanation, graphics, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }       
    
    static async updateLessonStepTutorialTitle(lessonId, contentId, newTitle) {
        return new Promise((resolve, reject) => {
            API.updateLessonStepTutorialTitle(lessonId, contentId, newTitle, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }      
    
    static async updateLessonStepExampleTitle(lessonId, contentId, newTitle) {
        return new Promise((resolve, reject) => {
            API.updateLessonStepExampleTitle(lessonId, contentId, newTitle, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }       

    static async insertLesson(topicId) {
        return new Promise((resolve, reject) => {
            API.insertLesson(topicId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }    

    static async insertLessonStepQuestion(lessonId, stepNumber, questionId, exampleId) {
        return new Promise((resolve, reject) => {
            API.insertLessonStepQuestion(lessonId, stepNumber, questionId, exampleId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }          
    
    static async cloneLessonStepQuestion(lessonId, stepNumber, questionId) {
        return new Promise((resolve, reject) => {
            API.cloneLessonStepQuestion(lessonId, stepNumber, questionId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }   
    
    static async deleteLessonStep(lessonId, id, type, contentId, number) {
        return new Promise((resolve, reject) => {
            API.deleteLessonStep(lessonId, id, type, contentId, number, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }     

    static async transposeLessonSteps(lessonId, id1, id2) {
        return new Promise((resolve, reject) => {
            API.transposeLessonSteps(lessonId, id1, id2, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }   
    
    static async getKeyPrerequisites(exampleId) {
        return new Promise((resolve, reject) => {
            API.getKeyPrerequisites(exampleId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }     

    static async updateKeyPrerequisites(exampleId, prerequisiteIds) {
        return new Promise((resolve, reject) => {
            API.updateKeyPrerequisites(exampleId, prerequisiteIds, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }       

    static async transferStudentAccountToSchool(studentId, schoolId) {
        return new Promise((resolve, reject) => {
            API.transferStudentAccountToSchool(studentId, schoolId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }   

    static async getUserSchool() {
        return new Promise((resolve, reject) => {
            API.getUserSchool((error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });        
        }); 
    }    

    static async getSchool(schoolId) {
        return new Promise((resolve, reject) => {
            API.getSchool(schoolId, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });        
        }); 
    }

    static async searchSchools(lookup) {
        return new Promise((resolve, reject) => {
            API.searchSchools(lookup, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }

    static async getNotificationPreferences(userKey) {
        return new Promise((resolve, reject) => {
            API.getNotificationPreferences(userKey, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });        
        }); 
    }

    static async updateNotificationPreferences(userKey, data) {
        return new Promise((resolve, reject) => {
            API.updateNotificationPreferences(userKey, data, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }    

    static async unsubscribeFromProductAnnouncements(userKey) {
        return new Promise((resolve, reject) => {
            API.unsubscribeFromProductAnnouncements(userKey, (error, response) => {
                if (error) {
                    resolve(null);
                } else {
                    resolve(response);
                }
            });
        });
    }
}