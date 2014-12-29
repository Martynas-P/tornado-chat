angular.module('chatApp', [])
    .controller('mainController', function($scope){
        $scope.username = '';

        $scope.messages = [];

        $scope.newMessage = null;

        var socket = new WebSocket('ws://localhost:8000/chat');

        socket.onmessage = function onMessage(data) {
            var message = JSON.parse(data.data);

            if (message.username) {
                $scope.username = message.username;
            } else if (message.from && message.message) {
                $scope.messages.push(message);
            }

            $scope.$apply();
        };

        $scope.sendMessage = function sendMessage() {
            if ($scope.newMessage) {
                socket.send($scope.newMessage);
            }

            $scope.newMessage = '';
        }
    });
