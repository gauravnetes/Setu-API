<script lang="ts">
  import type { SearchResult } from '$lib/types';
  import SearchResultCard from '$lib/SearchResultCard.svelte';

  let searchTerm = $state('');
  let isSearching = $state(false);
  let results = $state<SearchResult[]>([]);
  let error = $state<string | null>(null);
  let hasSearched = $state(false);

  let debounceTimeout: ReturnType<typeof setTimeout>;


  function mapFhirToSearchResult(fhirContains: any): SearchResult {
  const cleanResult: Partial<SearchResult> = {};

  // 1. Get the easy, top-level properties
  cleanResult.NAMASTE_Code = fhirContains.code;
  cleanResult.Traditional_Term = fhirContains.display;

  // 2. Loop through the 'designation' array to find the mapped data
  if (fhirContains.designation) {
    for (const des of fhirContains.designation) {
      // Use the 'use.code' to identify what each value means
      switch (des.use?.code) {
        case 'modern-name':
          cleanResult.Modern_Name = des.value;
          break;
        case 'icd11-biomed-code':
          cleanResult.ICD11_Biomedicine_Code = des.value;
          break;
        case 'icd11-tm2-code':
          cleanResult.ICD11_TM2_Code = des.value;
          break;
        case 'system':
          cleanResult.System = des.value;
          break;
        case 'description':
          cleanResult.Description = des.value;
          break;
      }
    }
  }

  return cleanResult as SearchResult;
}

  async function handleSearch() {
    if (!searchTerm.trim()) return;

    isSearching = true;
    error = null;
    hasSearched = true;

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/search?term=${searchTerm}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      
      // 1. Get the raw, complex FHIR response
      const rawFhirResponse = await response.json();

      // 2. Safely access the array of results inside the FHIR object
      const fhirResults = rawFhirResponse.expansion?.contains || [];

      // 3. Use our new mapping function to convert each complex result into a simple one
      results = fhirResults.map(mapFhirToSearchResult);

    } catch (e) {
      error = 'Failed to connect to the backend. Is the server running?';
      results = [];
    } finally {
      isSearching = false;
    }
  }


  function handleKeyPress(event: KeyboardEvent) {
    if (event.key === 'Enter') {
      handleSearch();
    }
  }

  // This function now correctly handles the quick search action
  function quickSearch(suggestion: string) {
    searchTerm = suggestion;
    handleSearch();
  }
</script>

<main
  class="relative flex min-h-screen flex-col items-center bg-gradient-to-b from-sky-100 to-white p-6"
>
  <!-- Header -->
  <div class="mb-8 w-full max-w-4xl text-center">
    <div class="mb-4 flex items-center justify-center gap-3">
      <img src="/logo.png" alt="My Company Logo" class="h-32" />
    </div>
    <p id="description" class="mb-4 text-lg text-gray-600">
      Translating Ancient Healing for a Modern World
    </p>
    <div class="flex items-center justify-center gap-4 text-sm text-gray-500">
      <span class="rounded-full bg-blue-100 px-3 py-1">Ministry of AYUSH</span>
    </div>
  </div>

  <!-- Main Search Card -->
  <div class="mb-8 w-full max-w-4xl rounded-3xl border-none bg-white p-8 shadow-xl">
    <!-- Search Bar -->
    <div class="mb-6 flex gap-3">
      <div class="relative flex-grow">
        <input
          id="search-input"
          type="text"
          bind:value={searchTerm}
          onkeypress={handleKeyPress}
          placeholder="🔍 Search for an AYUSH term (e.g., Amlapitta)..."
          class="rounded-4xl w-full border-none bg-blue-50 px-5 py-4 text-base shadow-sm transition-all duration-300 focus:border-sky-400 focus:outline-none focus:ring-2 focus:ring-sky-300"
        />
        {#if isSearching}
          <div class="absolute right-4 top-1/2 -translate-y-1/2 transform">
            <div
              class="h-5 w-5 animate-spin rounded-full border-2 border-sky-400 border-t-transparent"
            ></div>
          </div>
        {/if}
      </div>

      <button
        id="search-button"
        onclick={handleSearch}
        disabled={isSearching}
        class="rounded-4xl bg-sky-400 px-8 py-4 font-semibold text-white shadow-md transition-all duration-300 hover:bg-sky-500 hover:shadow-lg disabled:opacity-50"
      >
        {isSearching ? 'SEARCHING...' : 'SEARCH'}
      </button>
    </div>

    <!-- Quick Suggestions -->
    <div class="mb-8">
      <p class="mb-3 text-sm text-gray-500">Quick search:</p>
      <div class="flex flex-wrap gap-2">
        {#each ['Ardhavabhedaka', 'Suryavarta', 'Kasa', 'Pratishyaya', 'Abhishyanda', 'Tamaka Shwasa'] as suggestion}
          <!-- FIX 2: These buttons now correctly call the quickSearch function -->
          <button
            class="rounded-full border border-blue-200 bg-blue-100 px-4 py-2 text-sm text-sky-700 transition-colors hover:bg-blue-200"
            onclick={() => quickSearch(suggestion)}
          >
            {suggestion}
          </button>
        {/each}
      </div>
    </div>
  </div>
  
  <!-- FIX 3: Moved the entire results block OUTSIDE and BELOW the main search card for correct layout -->
  <div class="w-full max-w-4xl">
      {#if isSearching && !results.length}
        <p class="text-center text-gray-600">Searching...</p>
      {:else if error}
        <p class="text-center text-red-500 bg-red-100 p-4 rounded-xl">{error}</p>
      {:else if results.length > 0}
        {#each results as result (result.NAMASTE_Code)}
          <SearchResultCard {result} />
        {/each}
      {:else if hasSearched}
        <div class="text-center bg-white p-8 rounded-2xl border border-dashed">
            <h3 class="text-lg font-medium text-gray-700">No Results Found</h3>
            <p class="text-gray-500 mt-1">Try a different search term.</p>
        </div>
      {/if}
  </div>

  <!-- Footer -->
  <div class="mt-8 text-center text-gray-500">
    <p class="text-sm">Empowering Traditional Medicine Through Technology</p>
  </div>
</main>

<style>
  /* No changes needed here, your style block is perfect */
  @import url('https://fonts.googleapis.com/css2?family=Unbounded:wght@400;600;700;800&family=Space+Mono:wght@400;700&display=swap');

  #logo,
  #search-button {
    font-family: 'Unbounded', sans-serif;
    font-optical-sizing: auto;
  }

  #description,
  #search-input {
    font-family: 'Space Mono', monospace;
  }

  .glow {
    text-shadow: 0 0 8px rgba(56, 189, 248, 0.3);
  }
</style>