
var status = 'ready';

function getStatus() {
    // check status
//    $.ajax({
//        url: 'status.txt',
//        async: false,
//        success: function(data) {
//            status = data;
//        }
//    });

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
            if(getStatus() == 'ready') {
                this.vent.trigger("countdown")
            }
        },

        render: function() {
            status = 'ready';
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
            status = 'countdown';

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
            status = 'recording';

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
            status = 'processing';

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

        if (getStatus() == 'ready') {
            vent.trigger('countdown');
            return;
        }

    });



})(jQuery);




