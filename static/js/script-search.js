$(function() {
    var addTranscriptBlock = function(block_id, data) {
        var $header = $("<h3>", {
            id: block_id,
            class: "episode-head"
        });
        var $episodeName = $("<span>", {
            class: "episode", 
            text: data.title + " [" + data.series + "] "
        });
        var $location = $("<small>", {
            class: "text-muted",
            text: "We're in \"" + data.scene_location + "\""
        });
        var formatDialogueLine = function(data) {
            switch (Array.isArray(data)) {
                case true:
                    var dialogue = data[0] + ": " + data[1];
                    break;
                case false:
                    var dialogue = data;
                    break;
            };
            return dialogue;
        };
            
        // insert episode title and location into DOM
        $header.append($episodeName).append($location).appendTo("#dialogues")

        // insert dialogue block into DOM
        var $dialogue_block = $("<div>", {
            id: "dialogue-" + block_id,
            class: "dialogue-block"
        }).insertAfter($("#" + block_id));

        // add 2 lines before matched text
        $(data.lines_up).each(function() {
            console.log("switch case length: ", this.length, this, typeof(this));

            $("<p>", {
                class: "text-muted",
                text: formatDialogueLine(this)
            }).appendTo("#dialogue-" + block_id);
        });

        // add matched text to the div
        $("<p>", {
            style: "font-weight: bold;",
            text: data.speaker + ": " + data.match
        }).appendTo("#dialogue-" + block_id);

        // add 2 lines after matched text
        $(data.lines_down).each(function() {
            $("<p>", {
                class: "text-muted",
                text: formatDialogueLine(this)
            }).appendTo("#dialogue-" + block_id);
        });

        $("#dialogue-" + block_id).append("<hr class='mb-4'>");
    };

    $("#search_words").on("click", function(e) {
        e.preventDefault();

        if ($("#wordOrPhrase").val() == "") {
            alert("Search for something ya dummy!");
            return false;
        };
        
        var checkedboxes = [];

        $("input[type='checkbox']").each(function() {
            if ($(this).is(":checked")) {
                checkedboxes.push($(this).val());
            };
        });

        $.ajax({
            type: "GET", 
            url: "/search",
            data: {
                search: $("#wordOrPhrase").val(),
                series: JSON.stringify(series=checkedboxes)
            },
            success: function(result) {
                console.log(result);
                $("#matches").text(result.length);
                $("#dialogues").empty();

                var i = 0;

                $(result).each(function(e) {
                    addTranscriptBlock(i, this);
                    i++;
                    //$(".dialogue_block").append("<p class='dialogue_line'>" + this.match + "</p>");
                });
            },
            error: function(result) {
                console.log(result);
            }
        });
    });
});