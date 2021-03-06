// Reference: http://jasonwatmore.com/post/2014/05/26/angularjs-basic-http-authentication-example

// this is the model of the front end, cause Angular is Single Page Application, when you access different url, the model will load different ng-view which is view written in html, and the controller that view needed

angular
    .module('myApp', ['ngRoute', 'ngCookies','ng.confirmField','file-model'])
    .config(config)
    .run(run);
    
config.$inject = ['$routeProvider', '$locationProvider'];
function config($routeProvider, $locationProvider) {

    // show home page when accessing '/'
    $routeProvider.when('/',{
        templateUrl: 'main.html',
        controller:'homeController',
        controllerAs: 'vm'
    })

    // show login page when accessing '/login'
    .when('/login',{
        templateUrl: 'login.html',
        controller: 'loginController',
        controllerAs: 'vm'
    })

    // show sign up page when accessing '/sign up'
    .when('/signup',{
        templateUrl: 'signup.html',
        controller: 'registerController',
        controllerAs: 'vm'
    })

    // show current user's posts when accessing '/myposts'
    .when('/myposts',{
        templateUrl: 'myposts.html',
        controller: 'myPostController',
        controllerAs: 'vm'
    })

    // show currents user's friends list when accessing '/managefriends'
    .when('/managefriends',{
        templateUrl: 'manageFriends.html',
        controller: 'myFriendController',
        controllerAs: 'vm'
    })

    // show current user's information when accessing '/manageinfo'
    .when('/manageinfo',{
        templateUrl: 'manageInfo.html',
        controller: 'myInfoController',
        controllerAs: 'vm'
    })

    // show friend's post when accessing '/friendPost/id'
    .when('/friendPost/:id',{
        templateUrl: 'friendpost.html',
        controller: 'friendPostController',
        controllerAs: 'vm'
    })

    // if you enter some url other than above, back to home page
    .otherwise({
        redirectTo:'/'
    });
};

run.$inject = ['$rootScope', '$location', '$cookieStore', '$http'];
function run($rootScope, $location, $cookieStore, $http) {
    // keep user logged in after page refresh
    $rootScope.globals = $cookieStore.get('globals') || {};
    if ($rootScope.globals.currentUser) {
        $http.defaults.headers.common['Authorization'] = 'Basic ' + $rootScope.globals.currentUser.authdata; // jshint ignore:line
    }

    $rootScope.$on('$locationChangeStart', function (event, next, current) {
        // redirect to login page if not logged in and trying to access a restricted page
        if ($location.path() !== '/login' && !rootScope.globals.currentUser){
            $location.path('/login');
        }
    });
}
