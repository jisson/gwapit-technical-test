/**
 * Created by pierre on 30/10/2016.
 */

(function () {
  'use strict';

  angular
    .module('app.authentication.services')
    .factory('Authentication', Authentication);

  Authentication.$inject = ['$cookies', '$http'];

  /**
  * @namespace Authentication
  * @returns {Factory}
  */
  function Authentication($cookies, $http) {
    /**
    * @name Authentication
    * @desc The Factory to be returned
    */
    var Authentication = {
      logout: logout,
      unauthenticate: unauthenticate
    };

    return Authentication;

    ////////////////////

    /**
     * @name unauthenticate
     * @desc Delete the cookie where the user object is stored
     * @returns {undefined}
     * @memberOf app.authentication.services.Authentication
     */
    function unauthenticate() {
      delete $cookies.authenticatedAccount;
    }


    /**
     * @name logout
     * @desc Try to log the user out
     * @returns {Promise}
     * @memberOf app.authentication.services.Authentication
     */
    function logout() {
      return $http.post('/api/v1/auth/logout/')
        .then(logoutSuccessFn, logoutErrorFn);

      /**
       * @name logoutSuccessFn
       * @desc Unauthenticate and redirect to index with page reload
       */
      function logoutSuccessFn(data, status, headers, config) {
        Authentication.unauthenticate();
        window.location = '/';
      }

      /**
       * @name logoutErrorFn
       * @desc Log "Epic failure!" to the console
       */
      function logoutErrorFn(data, status, headers, config) {
        console.error('Epic failure!');
      }
    }

  }
})();