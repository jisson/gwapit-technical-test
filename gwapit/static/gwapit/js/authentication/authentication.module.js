/**
 * Created by pierre on 30/10/2016.
 */

(function () {
  'use strict';

  angular
    .module('app.authentication', [
      'app.authentication.services'
    ]);

  angular
    .module('app.authentication.services', ['ngCookies']);
})();