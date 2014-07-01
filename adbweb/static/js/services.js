var CRUD = {
	list: {method:'GET', isArray:true},
	create: {method:"POST"},
	read: {method:'GET'},
	update: {method:"PUT"},
	delete: {method:"DELETE"},
};

adbweb.factory('Deck', function($resource) {
	return $resource('deck/:deck_id', {deck_id: "@deck_id"}, CRUD);
});

adbweb.factory('Card', function($resource) {
	return $resource('card/:card_id', {card_id: "@card_id"}, CRUD);
});

adbweb.factory('User', function($resource) {
	return $resource('user/:user_id', {user_id: "@user_id"}, CRUD);
});
