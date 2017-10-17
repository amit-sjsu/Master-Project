'use strict';   // See note about 'use strict'; below

var myApp = angular.module('PredictionSystem', [
 'ngRoute',
]);

myApp.config(['$routeProvider',
     function($routeProvider) {
         $routeProvider.
             when('/', {
                 templateUrl: '../static/partials/prediction.html',
             }).
             when('/about', {
                 templateUrl: '../static/partials/about.html',
             }).
//             when('/login', {
//                 templateUrl: '../static/partials/login.html',
//                 controller: 'LoginController'
//             }).
//             when('/logout', {
//                 templateUrl: '../static/partials/home.html',
//                 controller: 'LogoutController'
//             }).
//             when('/signup', {
//                 templateUrl: '../static/partials/signup.html',
//                 controller: 'SignupController'
//             }).
//             when('/reports', {
//                 templateUrl: '../static/partials/reports.html',
//                 controller: 'ReportsController'
//             }).
             otherwise({
                 redirectTo: '/'
             });
    }]);