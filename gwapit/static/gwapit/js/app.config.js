/**
 * Created by pierre on 29/10/2016.
 */

(function () {
  'use strict';

  angular
      .module('app.config')
      .config(config);

  config.$inject = ['$locationProvider', '$interpolateProvider'];

  /**
   * @name config
   * @desc Enable HTML5 routing and override '{{ }}' operators to avoid conflicts in
   * Django templates.
   */
  function config($locationProvider, $interpolateProvider) {
    $locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!');

    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
  }
})();