/**
 * Created by pierre on 30/10/2016.
 */

(function() {
    'use strict';

    angular
        .module('app.layout.controllers')
        .controller('BodyController', BodyController);

    BodyController.$inject = ['$scope', 'EmailFactory'];

    /**
     *
     */
    function BodyController($scope, EmailFactory) {

        /**
         * Sort the given list based on object's 'internal_date' property.
         *
         * @param listToSort    The list to sort
         * @returns {Array}     The sorted list
         */
        function sortListByInternalDate(listToSort) {

            var sortedList = [];
            var map = new Map();
            var currentID = null;

            for (var i = 0; i < listToSort.length; i++) {
                var item = listToSort[i];
                if (item.previous_item_id === null) {
                    currentID = item.internal_date;
                    sortedList.push(item);
                } else {
                    map.set(item.previous_item_id, i);
                }
            }

            while (sortedList.length < listToSort.length) {

                var nextItem = listToSort[map.get(currentID)];
                sortedList.push(nextItem);
                currentID = nextItem.internal_date;
            }

            return sortedList;
        }

        $scope.retrieveEmailsStatus = "Loading...";
        $scope.showItem = false;

        var vm = this;
        EmailFactory.get100Emails()
            .success(function(emails) {

                $scope.emails = [];
                $scope.showItem = true;

                $scope.retrieveEmailsStatus = "";

                emails.forEach(function(email, i) {

                    var email_id = email.id;
                    EmailFactory.getEmailMessage(email_id).success(function(email)
                    {
                        $scope.emails[i] = email;
                    });
                });

                $scope.emails = sortListByInternalDate($scope.emails)
            })
            .error(function() {
                $scope.retrieveEmailsError = "Sorry, we can't retrieve your mails. Please try to log.";
                $scope.retrieveEmailsStatus = "";

                $scope.emails = [];
                $scope.showItem = false;
            });
    }
})();