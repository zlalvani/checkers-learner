'use strict';

angular.module('checkersLearnerApp', [
  'checkersLearnerApp.auth',
  'checkersLearnerApp.admin',
  'checkersLearnerApp.constants',
  'ngCookies',
  'ngResource',
  'ngSanitize',
  'ui.router',
  'ui.bootstrap',
  'validation.match'
])
  .config(function($urlRouterProvider, $locationProvider) {
    $urlRouterProvider
      .otherwise('/');

    $locationProvider.html5Mode(true);
  });
