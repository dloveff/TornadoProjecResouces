/**
 * Created by 閿﹀嘲 on 14-3-4.
 */

function init_index_module(appname) {
    return angular.module(appname, ['ngResource']);
}


var module = init_index_module('app');
init_rest_service(module);
init_nav_sign_tag(module);
//
//function init_authentication_controller(module) {
//    module.controller('authenticationCntl', ['$scope', 'passportService', 'signService', function ($scope, passportService, signService) {
//        $scope.signup = function(email, mobile, password) {
//            passportService.signup({ email: email, mobile:mobile, password: password }, function() {
//                $scope.passport = null;
//            });
//        };
//
//    }]);
//}
//