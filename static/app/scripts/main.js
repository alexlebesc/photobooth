
var STATUS_READY = 'READY';
var STATUS_COUNTDOWN = 'COUNTDOWN';
var STATUS_RECORDING = 'RECORDING';
var STATUS_PROCESSING = 'PROCESSING';
var status = STATUS_READY;

function getStatus() {
    // check status
    $.ajax({
        url: '/photobooth',
        async: false,
        type: 'JSON',
        success: function(data) {
            status = data;
        }
    });

    return status;
}

(function($){

    var vent = _.extend({}, Backbone.Events);

    var ReadyView = Backbone.View.extend({
        el: $('body'),

        initialize: function(options) {
            _.bindAll(this, 'render', 'goToCountDown');

            this.vent = options.vent;
            this.vent.bind("ready", this.render);

            var source   = $("#ready-template").html();
            this.template = Handlebars.compile(source);

        },

        goToCountDown: function() {
            if(getStatus() == STATUS_READY) {
                this.vent.trigger("countdown")
            }
        },

        render: function() {
            status = STATUS_READY;
            $(this.el).html(this.template());
        }
    });

    var CountDownView = Backbone.View.extend({
        el: $('body'),

        initialize: function(options) {
            _.bindAll(this, 'render');

            this.vent = options.vent;
            this.vent.bind("countdown", this.render);

            var source   = $("#countdown-template").html();
            this.template = Handlebars.compile(source);
        },

        render: function() {
            status = STATUS_COUNTDOWN;

            $(this.el).html(this.template());

            var $time = $('.front-countdown p');
            var time = $time.text();


            var countDown = setInterval(function() {
                if (parseInt(time) > 1) {
                    time = parseInt(time) - 1;
                    $time.text(time);
                }

            }, 1000);

            setTimeout(function() {
                clearInterval(countDown);
                vent.trigger('recording');
            }, 5000);
        }
    });

    var RecordingView = Backbone.View.extend({
        el: $('body'),

        initialize: function(options) {
            _.bindAll(this, 'render');

            this.vent = options.vent;
            this.vent.bind("recording", this.render);

            var source   = $("#recording-template").html();
            this.template = Handlebars.compile(source);
        },

        render: function() {
            status = STATUS_RECORDING;

            var pictureId = 0;

            var takePicture = setInterval(function() {

                pictureId += 1;

                $('.picture-frame-'+pictureId).show();

            }, 1000);

            setTimeout(function() {
                vent.trigger('processing');
                  clearInterval(takePicture);
            }, 5000);

            $(this.el).html(this.template());
        }
    });

    var ProcessingView = Backbone.View.extend({
        el: $('body'),

        initialize: function(options) {
            _.bindAll(this, 'render');

            this.vent = options.vent;
            this.vent.bind("processing", this.render);

            var source   = $("#processing-template").html();
            this.template = Handlebars.compile(source);
        },

        render: function() {
            status = STATUS_PROCESSING;

            setTimeout(function() {
                vent.trigger('ready');
            }, 5000);

            $(this.el).html(this.template());
        }
    });

    var readyView = new ReadyView({vent: vent});
    var countDownView = new CountDownView({vent: vent});
    var recordingView = new RecordingView({vent: vent});
    var processingView = new ProcessingView({vent: vent});

    readyView.render();

    $(document).on('click', function() {

        if (getStatus() == STATUS_READY) {
            vent.trigger('countdown');
            return;
        }

    });


})(jQuery);




