(function() {

    function escapeHtml(value) {
        return String(value || '')
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    function displaySearchResults(results, store) {
        var searchResults = document.getElementById('search-results');

        if (results.length) {
            var appendString = '<h2>What I found for you</h2>';

            appendString += '<p>' + results.length + ' articles found.</p>';

            for (var i = 0; i < results.length; i++) {
                var item = store[results[i].ref];

                // Determine article source
                var isWiki = item.collection === 'wiki';

                var badge = isWiki
                    ? '<span class="search-badge badge-wiki">IT-Wiki</span>'
                    : '<span class="search-badge badge-blog">PowerShell</span>';

                // Article title and source badge
                appendString += '<h3 class="search-result-title">';
                appendString += '<a href="' + escapeHtml(item.url) + '">';
                appendString += escapeHtml(item.title);
                appendString += '</a>';
                appendString += badge;
                appendString += '</h3>';

                // Category and content preview
                appendString += '<p>';
                appendString += '<b>' + escapeHtml(item.category) + ' </b>';
                appendString += escapeHtml(
                    (item.content || '').substring(0, 50)
                );
                appendString += '...</p>';
            }

            searchResults.innerHTML = appendString;

        } else {
            searchResults.innerHTML = '<p>No results found</p>';
        }
    }

    function getQueryVariable(variable) {
        var params = new URLSearchParams(window.location.search);
        return params.get(variable);
    }

    var searchTerm = getQueryVariable('query');

    if (searchTerm) {
        document.getElementById('search-box').value = searchTerm;

        // Initialize Lunr search index
        var idx = lunr(function() {
            this.field('id');
            this.field('title', { boost: 10 });
            this.field('author');
            this.field('category');
            this.field('content');
        });

        // Add all documents to the search index
        for (var key in window.store) {
            idx.add({
                'id': key,
                'title': window.store[key].title,
                'author': window.store[key].author,
                'category': window.store[key].category,
                'content': window.store[key].content
            });
        }

        // Execute search after completing the index
        var results = idx.search(searchTerm);

        // Display search results
        displaySearchResults(results, window.store);
    }

})();