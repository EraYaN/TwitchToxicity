<script id="message-template" type="text/x-handlebars-template">
    <div class="col-12 col-md-12 message {{#if (gt num_classifications 0)}}message-classified{{/if}}" id="message{{message_id}}" data-message-id="{{message_id}}">
        <div class="row">
            <div class="col-md-1">
                <small>#{{message_id}} <span id="message-classification{{message_id}}">{{users}} ({{num_classifications}})</span></small>
            </div>
            <div class="col-md-7">
                <p class="">From <strong>{{message_data.attributes.from}}</strong>: {{{message_data.attributes.message-diff}}}</p>
            </div>
            <div class="col-md-4">
                <div class="btn-group float-right" role="group" aria-label="Classification Buttons">
                    <button type="button" data-toggle="button" aria-pressed="false" autocomplete="off" class="btn btn-secondary message-button{{message_id}} {{#if (eq classification 1)}}active{{/if}}" onclick="submit_classification({{message_id}},this.value); return false;" value="1">1</button>
                    <button type="button" data-toggle="button" aria-pressed="false" autocomplete="off" class="btn btn-secondary message-button{{message_id}} {{#if (eq classification 2)}}active{{/if}}" onclick="submit_classification({{message_id}},this.value); return false;" value="2">2</button>
                    <button type="button" data-toggle="button" aria-pressed="false" autocomplete="off" class="btn btn-secondary message-button{{message_id}} {{#if (eq classification 3)}}active{{/if}}" onclick="submit_classification({{message_id}},this.value); return false;" value="3">3</button>
                    <button type="button" data-toggle="button" aria-pressed="false" autocomplete="off" class="btn btn-secondary message-button{{message_id}} {{#if (eq classification 4)}}active{{/if}}" onclick="submit_classification({{message_id}},this.value); return false;" value="4">4</button>
                    <button type="button" data-toggle="button" aria-pressed="false" autocomplete="off" class="btn btn-secondary message-button{{message_id}} {{#if (eq classification 5)}}active{{/if}}" onclick="submit_classification({{message_id}},this.value); return false;" value="5">5</button>
                </div>
            </div>
        </div>

    </div>
</script>
<div class="row">
    <div class="col-12 col-md-8">
        <form class="form-inline">
            <label class="sr-only" for="num_entries">Number of entries</label>
            <div class="input-group mb-2 mr-sm-2 mb-sm-0">
                <div class="input-group-addon">Entries</div>
                <input type="number" step="1" min="10" max="200" class="form-control mb-2 mr-sm-2 mb-sm-0" id="num_entries" placeholder="Entries" value="25">
            </div>
            <label class="sr-only" for="context_num">Context number</label>
            <div class="input-group mb-2 mr-sm-2 mb-sm-0">
                <div class="input-group-addon">Context</div>
                <input type="number" step="1" min="0" max="50" class="form-control mb-2 mr-sm-2 mb-sm-0" id="context_num" placeholder="Context" value="5">
            </div>
            <div class="form-check mb-2 mr-sm-2 mb-sm-0">
                <label class="form-check-label">
                    <input class="form-check-input" type="checkbox" id="full_update" checked> Full update
                </label>
            </div>
        </form>
    </div>
    
</div>
<div class="row" id="classifier">
    <div class="col-12 col-md-12">
        <h3>Messages</h3><button class="btn btn-sm btn-secondary" onclick="refresh(); return false;">Refresh</button>
        
        
        <div class="row" id="messages_container">

        </div>
    </div>
</div>

