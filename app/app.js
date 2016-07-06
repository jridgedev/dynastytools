'use strict';

var teamModule = angular.module('teamModule', []);

teamModule.controller('TeamListController', function PhoneListController($scope, $http) {
  $scope.teams = [];
  $http.get('json/leagueTeams.json').success(function(data) {
	$scope.teams = $.parseJSON(data).teams;
  });
});