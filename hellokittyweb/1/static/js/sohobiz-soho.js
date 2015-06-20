/**
 * Created by 閿﹀嘲 on 14-3-9.
 */

function init_soho_module(appname) {
    return angular.module(appname, ['ngResource', 'ngRoute']);
}

function init_soho_routes(module) {
    module.config(['$routeProvider', '$locationProvider', function ($routeProvider, $locationProvider) {
        $routeProvider.when('/first', {
            templateUrl: function(params) { console.log(params);return 'soho-first-view.html';},
            controller: 'routeCntl'
        }).when('/plus', {
            templateUrl: 'soho-plus-view.html',
            controller: 'routeCntl'
        }).when('/friends', {
            templateUrl: 'soho-friends-view.html',
            controller: 'routeCntl'
        }).when('/favor', {
            templateUrl: 'soho-favor-view.html',
            controller: 'routeCntl'
        }).when('/settings', {
            templateUrl: 'soho-settings-view.html',
            controller: 'routeCntl'
        }).when('/office/:officeId', {
            templateUrl: 'soho-office-view.html',
            controller: 'officeDetailCntl'
        }).otherwise({
            redirectTo: '/first'
        });

        $locationProvider.html5Mode(false);
    }]);
}

function init_soho_controllers(module) {
    module.controller('officeCntl', ['$scope', 'officeService', function ($scope, officeService) {
        $scope.offices = officeService.query();
    }]).controller('officeDetailCntl', ['$scope', '$routeParams', 'officeService', function ($scope, $routeParams, officeService) {
        $scope.officeId = $routeParams.officeId;
        $scope.office = officeService.get({officeId: $scope.officeId});
    }]).controller('officeFunctionCntl', ['$scope', '$rootScope', '$routeParams', 'officeService', function ($scope, $rootScope, $routeParams, officeService) {
        return $rootScope.$on("$routeChangeSuccess", function(event, current) {
            if (($routeParams != {}) && ('officeId' in $routeParams)) {
                $scope.officeId = $routeParams.officeId;
                $scope.office = officeService.get({officeId: $scope.officeId});
            }
        });
    }]).controller('routeCntl', ['$scope', '$routeParams', '$location', function ($scope, $routeParams, $location) {
        $scope.location = $location;

        // TODO 妯℃嫙鏁版嵁锛屽悗缁渶瑕佽皟鏁村鑸潯
        $scope.routes = [{name: '涓€灞�', path:'#/test'}, {name: '浜屽眰', path:'#/testx'}, {name: '涓夊眰'}];
    }]);
}

var module = init_soho_module('app');
init_rest_service(module);
init_soho_routes(module);
init_nav_sign_tag(module);
init_soho_controllers(module);

