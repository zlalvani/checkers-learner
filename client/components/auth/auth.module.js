'use strict';

angular.module('checkersLearnerApp.auth', [
  'checkersLearnerApp.constants',
  'checkersLearnerApp.util',
  'ngCookies',
  'ui.router'
])
  .config(function($httpProvider) {
    $httpProvider.interceptors.push('authInterceptor');
  });
