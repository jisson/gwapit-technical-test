

(function() {
    'use strict';

    angular
        .module('app.resource.factories')
        .factory('EmailFactory', EmailFactory);

    EmailFactory.$inject = ['$http'];

    /**
     *  Factory for emails objects.
     */
    function EmailFactory($http) {

        return {

            get100Emails: function()
            {
                return $http.get('api/v1/resource/emails/');
            },

            getEmailMessage: function(messageId)
            {
                return $http.get('api/v1/resource/emails/' + messageId + '/');
            }
        }
    }

})();