/**
 * Created by 閿﹀嘲 on 14-3-9.
 */

function init_rest_service(module) {
    module.factory('passportService', ['$resource', function($resource) {
        return $resource('/passport', {}, {
            get: { method: 'GET' },
            update: { method: 'PUT' },
            signup: { method: 'POST' }
        });
    }]).factory('signService', ['$resource', function($resource) {
        return $resource('/sign', {}, {
            signin: { method: 'POST' },
            signout: { method: 'DELETE' }
        });
    }]).factory('officeService', ['$resource', function($resource) {
        return $resource('/office/:officeId', {}, {
            get: { method:'GET', params: {officeId: 0}, isArray: false },
            query: { method: 'GET', isArray: true },
            create: { method: 'POST' },
            update: { method: 'PUT', params: {officeId: '@id'} },
            delete: { method: 'DELETE', params: {officeId: '@id'} }
        });
    }]);
}

function init_nav_sign_tag(module) {
    module.directive('navSign', ['passportService', 'signService', function(passportService, signService) {
        return {
            restrict: 'AE',
            scope: {},
            templateUrl: '/navsign.inc.html',
            link: function (scope, element, attrs) {
                passportService.get(function(rt) {
                    scope.passport = rt;
                }, function() {
                    scope.passport = null;
                });

                scope.signin = function(email, password) {
                    signService.signin({ email: email, password: password }, function(rt) {
                        scope.passport = rt;
                    }, function () {
                        $('#signin-form-email').tooltip({
                            animation: true,
                            placement: 'bottom',
                            trigger: 'manual',
                            title: '鐧婚檰澶辫触'
                        });
                        $('#signin-form-email').tooltip('show');
                        setTimeout(function() {
                            $('#signin-form-email').tooltip('destroy');
                        }, 3000);
                    });
                };

                scope.signout = function() {
                    signService.signout(function() {
                        scope.passport = null;
                    });
                };
            }
        };
    }]).controller('signCntl', function () {});
}