'use strict';

(function() {

class MainController {

  constructor($http) {
    this.$http = $http;

  }


}

angular.module('checkersLearnerApp')
  .controller('MainController', MainController);

})();
