(function (root, factory) {
	if (typeof define === 'function' && define.amd) {
		// AMD. Register as an anonymous module.
		define('bzr-vb-dialogs', [], factory);
	} else {
		// Browser globals
		root.BZRVbDialogs = factory();
	}
})(window, function () {
	var $ = jQuery;

	function requirecss(file) {
		var link = document.createElement("link");
		link.type = "text/css";
		link.rel = "stylesheet";
		link.href = file;
		document.getElementsByTagName("head")[0].appendChild(link);
	}

	return {
		init: function (opt) {
			var externalDfd = new $.Deferred,
				requireController = new $.Deferred(),
				loadContent;

			var version = opt.version,
				objectId = opt.objectId | 0,
				objectType = opt.objectType,
				$container = opt.$container,
				isOwner = !!opt.isOwner,
				canPostQuestion = !!opt.canPostQuestion;

			if (!objectId || !objectType || !$container.length) {
				externalDfd.fail("You have to pass objectId, objectType and $container options to API");
			}

			var urlConfig = {
				'host': 'https://my.drom.ru',
				'createDialogUrl': 'https://my.drom.ru/personal/messaging/drom/ask/__type__/__id__',
				'replyInDialogUrl': 'https://my.drom.ru/personal/messaging/drom/reply/__dialogId__'
			};

			var ReplyingVisibilityType = {
				PUBLIC: 'public',
				PRIVATE: 'private',
				UNDEFINED: 'undefined'
			};

			var url = 'https://my.drom.ru/personal/messaging/drom/export/__type__/__id__'
				.replace('__type__', objectType)
				.replace('__id__', objectId);

			requirecss('https://static.baza.drom.ru/resources/styles/scss/messaging/messaging_drom_dk.css?2004746560');

			requirejs.config({
				paths: {
					'bzr-photo-swipe': 'https://static.baza.drom.ru/resources/js/photo-swipe/photo-swipe.js?2000803609'
				}
			});

			if (typeof requirejs === 'function' && define.amd) {
				requirejs(['https://static.baza.drom.ru/resources/js/drom-messaging.js?2000386740'], function (DromMessagingApiController) {
					requireController.resolve(DromMessagingApiController);
				}, function () {
					requireController.reject();
				});
			} else {
				$.ajax({url: 'https://static.baza.drom.ru/resources/js/drom-messaging.js?2000386740', dataType: "script", cache: true}).done(function () {
					requireController.resolve(window.DromMessagingApiController);
				}).fail(function () {
					requireController.reject();
				})
			}

			loadContent = $.ajax({
				url: url,
				data: {version: version},
				xhrFields: {withCredentials: true}
			});

			$.when(requireController, loadContent)
				.done(function (DromMessagingApiController, responseArr) {
					var content = responseArr[0],
						controller;

					// для незалогиненных дром оставляет свою форму со сценарием логина, она внутри контейнера
					// чтобы диалоги были над ней нужно делать prepend
					$container.prepend(content);

					controller = new DromMessagingApiController(
						urlConfig, ReplyingVisibilityType, $container, objectType, objectId, !!isOwner, version, canPostQuestion
					)
					controller.start();
					externalDfd.resolve();
				})
				.fail(function () {
					externalDfd.reject();
				});

			return externalDfd.promise();
		}
	}
});