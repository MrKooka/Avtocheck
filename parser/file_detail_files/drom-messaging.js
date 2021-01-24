(function (root, factory) {
	if (typeof define === 'function' && define.amd) {
		define([], factory);
	} else {
		root.DromMessagingApiController = factory();
	}
})(window, function () {
	/**
	 * @param {Object}	urlConfig		урлЫ
	 * @param {Object}	ReplyingVisibilityType типы видимости ответа on reply
	 * @param {jQuery}	$container
	 * @param {string}	objectType		тип объекта, к которому привязываются диалоги
	 * @param {int} 	objectId		ID
	 * @param {bool}	isOwner			является ли просматривающий владельцем объявления. !!! в зависимости от
	 * 									значения можно альтерить UI, но не отправлять на backend
	 * @param {bool}	deviceVersion	мобильная или десктопная версия ("mobile", "desktop" соответственно)
	 * @param {bool}    canPostQuestion Можно ли задавать вопрос
	 * @constructor
	 */
	function DromMessagingApiController(
		urlConfig,
		ReplyingVisibilityType,
		$container,
		objectType,
		objectId,
		isOwner,
		deviceVersion,
		canPostQuestion
	) {
		this.initialized = false;
		this.$container = $container;
		this.objectType = objectType + '';
		this.objectId = objectId | 0;
		this.viewerIsOwner = !!isOwner;
		this.deviceVersion = deviceVersion;
		this.canPostQuestion = !!canPostQuestion;
		this.ReplyingVisibilityType = ReplyingVisibilityType; /* need to be private ?*/

		this.ui = {
			$askQuestionLink: null,
			$askQuestionWrapper: null,
			$form: null,
			$errorHolder: null,
			$loginHiddenNote: null,
			$visibilityControl: null
		};

		// конфиг
		this.host = urlConfig.host;
		this.createDialogUrl = urlConfig.createDialogUrl;
		this.replyInDialogUrl = urlConfig.replyInDialogUrl;
	}

	/**
	 * Инициализация API — заполняем конфиг, вешаем обработчики эвентов
	 * @public
	 */
	DromMessagingApiController.prototype.start = function () {
		if (this.initialized) {
			return;
		}

		if (this.deviceVersion === 'desktop') {
			this.$container.addClass('bzr-dialog__container_desktop');
		}

		// заполняем ссылки на UI элементы, с которыми собираемся работать
		this.ui.$askQuestionLink = this.$container.find('[data-action="ask-question"]');
		this.ui.$askQuestionWrapper = this.$container.find('#bzr-ask_question_wrapper');
		this.ui.$form = this.ui.$askQuestionWrapper.find('form');
		this.ui.$errorHolder = this.$container.find('[data-role="error-holder"]');
		this.ui.$loginHiddenNote = this.$container.find('[data-name="login-hidden-note"]');
		this.ui.$visibilityControl = this.ui.$form.find('[data-role="visibility-control"]');

		// подстраиваем UI под переданный конфиг
		this.ui.$askQuestionLink.toggle(!this.viewerIsOwner && this.canPostQuestion);
		this.ui.$loginHiddenNote.toggle(!this.viewerIsOwner);

		// Вешаем обработчики эвентов
		this.$container.on('click', '[data-action="ask-question"]', $.proxy(this.handleAsk, this));
		this.$container.on('click', '[data-action="reply"]', $.proxy(this.handleReply, this));
		this.$container.on('click', '[data-action="report-spam"]', $.proxy(this.reportSpam, this));
		this.$container.on('click', '[data-action="show-dialog"]', $.proxy(this.toggleVisibility, this));
		this.$container.on('click', '[data-action="hide-dialog"]', $.proxy(this.toggleVisibility, this));
		this.$container.on('click', '[data-action="remove"]', $.proxy(this.removeToggle, this));
		this.$container.on('click', '[data-action="restore"]', $.proxy(this.removeToggle, this));
		this.$container.on('click', '[data-action="remove-as-spam"]', $.proxy(this.removeAsSpam, this));

		this.ui.$form.on('submit', $.proxy(this.handleSubmit, this));

		// done!
		this.initialized = true;

		// так как контент асинхронный скроллиться по якорю диалог не будет, нужно делать это ручками
		this.scrollToDialog();
	};

	DromMessagingApiController.prototype.performAction = function (event, successCallback) {
		event.preventDefault();
		event.stopPropagation();

		var $actionBtn = $(event.currentTarget),
			actionUrl = $actionBtn.attr('href');

		var $dialog = $actionBtn.closest('.bzr-dialog');

		if ($actionBtn.hasClass('bzr-dialog__control_loading')) {
			return;
		}

		if (actionUrl.indexOf('://') === -1) {
			actionUrl = this.host + actionUrl;
		}

		$actionBtn.addClass('bzr-dialog__control_loading');

		$.ajax({
			url: actionUrl,
			dataType: 'json',
			data: {ajax: 1, viewBullMode: 1},
			xhrFields: {withCredentials: true},
			context: this
		})
			.done(function (response) {
				this.removeStartupDialogActions($dialog);
				successCallback.call(this, response, $dialog);
			})
			.always(function () {
				$actionBtn.removeClass('bzr-dialog__control_loading');
			});
	};

	DromMessagingApiController.prototype.toggleVisibility = function (event) {
		this.performAction(event, function (response, $dialog) {
			if (response.status != 200) {
				return;
			}

			var $actions = this.updateActions($dialog, response),
				// если в новом свиске действий есть скрытие, значит диалог публичный
				isPublic = $actions.find('[data-action="hide-dialog"]');

			// в диалоге могло быть предложение опубликовать диалог, его надо скрыть, если диалог стал публичным
			$dialog.find('.bzr-dialog__system-message[data-role="proposal-to-publish-dialog"]').toggle(!isPublic);
		});
	};

	DromMessagingApiController.prototype.reportSpam = function (event) {
		this.performAction(event, function (response, $dialog) {
			if (response.status != 200) {
				return;
			}

			this.updateActions($dialog, response);
		});
	};

	DromMessagingApiController.prototype.removeToggle = function (event) {
		this.performAction(event, function (response, $dialog) {
			if (response.status != 200) {
				return;
			}

			this.updateActions($dialog, response);
		});
	};

	DromMessagingApiController.prototype.removeAsSpam = function (event) {
		this.performAction(event, function (response, $dialog) {
			if (response.status != 200) {
				return;
			}

			this.updateActions($dialog, response);
		});
	};

	DromMessagingApiController.prototype.handleAsk = function (event) {
		event.preventDefault();
		event.stopPropagation();

		this.clearErrors();
		this.ui.$askQuestionWrapper.attr('data-did', null);
		this.ui.$askQuestionWrapper.appendTo(this.$container);
		this.ui.$visibilityControl.hide();
		this.ui.$askQuestionWrapper.show();

		// focus input
		this.deviceVersion === 'desktop' && this.ui.$form.find('textarea[name="text"]').focus();
	};

	DromMessagingApiController.prototype.handleReply = function (event) {
		var $target, $dialog;

		event.preventDefault();
		event.stopPropagation();

		$target = $(event.currentTarget);
		$dialog = $target.closest('.bzr-dialog');

		this.clearErrors();
		this.ui.$askQuestionWrapper.attr('data-did', $target.attr('data-did')); // dialogId
		this.ui.$askQuestionWrapper.attr('data-hash', $dialog.find('.bzr-dialog__msg-container:last-child').attr('data-hash')); // latest message hash
		this.ui.$visibilityControl.toggle(this.viewerIsOwner);

		this.ui.$askQuestionWrapper.insertAfter($dialog);
		this.ui.$askQuestionWrapper.show();

		// focus input
		this.deviceVersion === 'desktop' && this.ui.$form.find('textarea[name="text"]').focus();
	};

	DromMessagingApiController.prototype.handleSubmit = function (event) {
		var text, dialogId, request, latestMessageHash, visibilityType, $target;

		event.preventDefault();
		event.stopPropagation();

		$target = $(event.currentTarget);

		if (true === $target.prop('disabled')) {
			return;
		}

		$target.prop('disabled', true);
		text = this.ui.$form.find('textarea[name="text"]').val();
		dialogId = this.ui.$askQuestionWrapper.attr('data-did') | 0;

		if (dialogId > 0) {
			latestMessageHash = this.ui.$askQuestionWrapper.attr('data-hash');
			visibilityType = this.ui.$visibilityControl.find(':checked:visible').val();
			request = this.reply(text, dialogId, latestMessageHash, visibilityType);
		} else {
			request = this.askSeller(text);
		}

		this.clearErrors();

		request
			.done(function (response) {

				if (406 === response.status) {
					this.showErrors(response.violations);
				}

				if (200 === response.status) {
					var $dialog = this.getDialog(response.dialogId | 0),
						isDialogPublic;

					if ($dialog.length > 0) {
						this.insertMessagesToDialog(response.content, $dialog);
						this.removeStartupDialogActions($dialog);
						isDialogPublic = visibilityType === this.ReplyingVisibilityType.PUBLIC;

						if (this.viewerIsOwner && isDialogPublic) { /* если владелец и это reply, то */
							 $dialog.find('.bzr-dialog__system-message[data-role="proposal-to-publish-dialog"]').remove();
						}

						this.updateActions($dialog, response);
					} else {
						this.insertDialog(response.content);
					}

					this.hideForm();
					this.triggerApiEvent('message-sent');
				}
			})
			.fail(function (response) {
				// what do we do?
			})
			.always(function () {
				$target.prop('disabled', false);
			});
	};

	DromMessagingApiController.prototype.askSeller = function (text) {

		var url = this.createDialogUrl
			.replace('__type__', this.objectType)
			.replace('__id__', this.objectId);

		var data = {
			ajax: 1,
			text: text
		};

		return $.ajax({
			context: this,
			method: 'POST',
			type: 'POST',
			url: url,
			data: data,
			xhrFields: {withCredentials: true}
		});
	};

	DromMessagingApiController.prototype.reply = function (text, dialogId, latestMessageHash, visibilityType) {

		var url = this.replyInDialogUrl
			.replace('__dialogId__', dialogId);

		var data = {
			ajax: 1,
			text: text,
			latestMsgHash: latestMessageHash,
			replyingVisibilityType: visibilityType || 'undefined' /* maybe todo const ?*/
		};

		return $.ajax({
			context: this,
			method: 'POST',
			type: 'POST',
			url: url,
			data: data,
			xhrFields: {withCredentials: true}
		});
	};

	DromMessagingApiController.prototype.updateActions = function ($dialog, response) {
		var $actions = $(response.actions);

		if ($actions.length > 0) {
			$dialog.find('[data-role=dialog-actions]').replaceWith($actions);
		} else {
			$actions = $dialog.find('[data-role=dialog-actions]');
		}

		if (response.message) {
			this.showFlash($actions, response.message);
		}

		return $actions;
	};

	DromMessagingApiController.prototype.showFlash = function ($actions, message) {
		var $notify = $('<div>', {
			'class': 'bzr-dialog__panel-block bzr-dialog-actions__notify',
			'html': message
		});

		$actions.append($notify);

		setTimeout(function () {
			$notify.remove();
		}, 2000);
	};

	DromMessagingApiController.prototype.scrollToDialog = function () {
		var _this = this,
			dialog,
			match = /#bzr\-dialog\-(\d+)/i.exec(document.location.hash);

		if (
			"function" !== typeof this.$container.get(0).scrollIntoView ||
			!match || !match.length
		) {
			return;
		}

		dialog = _this.getDialog(match[1] | 0).get(0);
		dialog && dialog.scrollIntoView(true);
	};
	
	DromMessagingApiController.prototype.clearErrors = function () {
		this.ui.$errorHolder.empty();
	};
	
	DromMessagingApiController.prototype.showErrors = function (errorList) {
		if (!errorList || !errorList.length) {
			return;
		}

		var prototype = this.ui.$errorHolder.attr('data-prototype');

		$.prototype.append.apply(
			this.ui.$errorHolder,
			$.map(errorList, function (errorMsg) {
				return prototype.replace('{{ err }}', errorMsg);
			})
		);
	};

	DromMessagingApiController.prototype.insertMessagesToDialog = function (messagesMarkup, $dialog) {
		if (!messagesMarkup || !messagesMarkup.length) {
			return;
		}

		$.prototype.append.apply(
			$dialog.children('.bzr-dialog__inner'),
			messagesMarkup
		);
	};

	DromMessagingApiController.prototype.insertDialog = function (markup) {
		if (!markup) {
			return;
		}

		this.ui.$askQuestionLink.parent().before(markup);
	};

	DromMessagingApiController.prototype.getDialog = function (id) {
		return this.$container.find('#bzr-dialog-'+id);
	};

	DromMessagingApiController.prototype.hideForm = function () {
		this.ui.$askQuestionWrapper.hide();
		this.ui.$form.get(0).reset();
	};

	DromMessagingApiController.prototype.removeStartupDialogActions = function ($dialog) {
		$dialog.find('[data-role="startup-actions"]').remove();
	};

	DromMessagingApiController.prototype.triggerApiEvent = function (eventName, detail) {
		try {
			var initDict = {
				'detail': Object.assign({
					objectType: this.objectType,
					objectId: this.objectId,
					viewerIsOwner: this.viewerIsOwner,
					deviceVersion: this.deviceVersion
				}, detail || {})
			};

			this.$container.get(0).dispatchEvent(new CustomEvent(eventName + ".bzr-messaging", initDict))
		} catch (e) {
			console && console.error("Messaging: event dispatch failed", e);
		}
	};

	return DromMessagingApiController;
});