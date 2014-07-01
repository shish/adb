
adbweb.controller("MainCtrl", function($scope, $routeParams, Deck, Card, User) {
	$scope.current_user = User.read({user_id: 1});
	$scope.decks = Deck.list();

	$scope.$on('$routeChangeSuccess', function (event, routeData) {
		if($routeParams.deck_id) {
			$scope.deck = Deck.read({deck_id: $routeParams.deck_id});
		}
		else {
			$scope.deck = null;
		}
		if($routeParams.card_id) {
			$scope.card = Card.read({card_id: $routeParams.card_id});
		}
		else {
			$scope.card = null;
		}
	});
});

adbweb.controller("HeaderCtrl", function($scope, $routeParams, Deck, User) {
	$scope.session_create = function() {
		$scope.current_user = User.read({user_id: 1});
	};
	$scope.session_delete = function() {
		$scope.current_user = null;
	};
});

adbweb.controller("UserReadCtrl", function($scope, $routeParams, User) {
	$scope.user = User.read({user_id: $routeParams.user_id});

	$scope.user_update = function() {
		User.update($scope.user);
	}
});


adbweb.controller("DeckListCtrl", function($scope, Deck) {
	$scope.decks = Deck.list();
});

adbweb.controller("DeckCreateCtrl", function($scope, $route, $routeParams, Deck) {
	var blank_deck = {
		title: "",
        type: "user",
	};

	$scope.deck = angular.copy(blank_deck);
	$scope.save = function() {
		Deck.create($scope.deck, function(response) {
			$scope.deck.deck_id = response.deck_id;
			$scope.decks.push($scope.deck);
			$scope.deck = angular.copy(blank_deck);
		});
	};
});

adbweb.controller("DeckReadCtrl", function($scope, $routeParams, Deck) {
	$scope.deck = Deck.read({deck_id: $routeParams.deck_id});

	$scope.save = function() {
		Deck.update(angular.copy($scope.deck), function() {
			//alert("Saved");
		});
	};

    $scope.incLink = function(link) {
        if(link.number < 4) {
            link.number = link.number + 1;
        }
    }
    $scope.decLink = function(link) {
        if(link.number > 0) {
            link.number = link.number - 1;
        }
    }
    $scope.delLink = function(link) {
        console.log("Not implemented");
    }
});


adbweb.controller("CardListCtrl", function($scope, Card) {
	$scope.cards = Card.list();
});

adbweb.controller("CardCreateCtrl", function($scope, $route, $routeParams, $location, Card) {
	$scope.card = {
		deck_id: $routeParams.deck_id,
	};

	$scope.create = function() {
		Card.create($scope.card, function(response) {
			$scope.card.card_id = response.card_id;
			$location.path("/deck/"+$scope.card.deck_id+"/card/"+$scope.card.card_id);
		});
	};
});

adbweb.controller("CardReadCtrl", function($scope, $routeParams, Card) {
	$scope.card = Card.read({card_id: $routeParams.card_id});

	$scope.save = function() {
		Card.update(angular.copy($scope.card), function() {
			//alert("Saved");
		});
	};
});
