adbweb.config(['$routeProvider', function($routeProvider) {
	$routeProvider.
		when('/deck', {templateUrl: 'static/partials/deck-list.html', controller: "DeckListCtrl"}).
		when('/deck/:deck_id', {templateUrl: 'static/partials/deck-read.html', controller: "DeckReadCtrl"}).
		when('/card', {templateUrl: 'static/partials/card-list.html', controller: "CardListCtrl"}).
		when('/card/:card_id', {templateUrl: 'static/partials/card-read.html', controller: "CardReadCtrl"}).
		when('/user/:user_id', {templateUrl: 'static/partials/user-read.html', controller: "UserReadCtrl"}).
		otherwise({redirectTo: '/deck'});
}]);
