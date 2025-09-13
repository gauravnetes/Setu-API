<script lang="ts">
  import type { SearchResult } from './types';
  export let result: SearchResult;
</script>

<div class="mb-4 rounded-2xl border border-blue-100 bg-white p-6 shadow-lg transition-all hover:shadow-xl hover:border-sky-300">
  <div class="flex flex-col md:flex-row md:items-start gap-6">
    <div class="flex-grow">
      <span class="rounded-full bg-sky-100 text-sky-800 px-3 py-1 text-xs font-semibold">{result.System}</span>
      <h2 class="mt-2 text-2xl font-bold text-gray-800">{result.Traditional_Term}</h2>
      <p class="mt-1 text-gray-600 font-mono">{result.NAMASTE_Code}</p>
      <p class="mt-2 text-sky-400 font-bold">{result.Modern_Name}</p>
      <p class="mt-2 text-gray-700">{result.Description}</p>
    </div>
    
    <div class="flex-shrink-0 w-full md:w-64 bg-blue-50 rounded-xl p-4 border border-blue-200">
      <h3 class="text-sm font-semibold text-gray-500 mb-2">MAPPED CODES</h3>
      {#if result.ICD11_Biomedicine_Code}
        <div class="mb-2">
          <p class="font-mono text-blue-800 bg-blue-200 rounded px-2 py-1 inline-block">{result.ICD11_Biomedicine_Code}</p>
          <p class="text-xs text-gray-500 mt-1">ICD-11 (Biomedicine)</p>
        </div>
      {/if}
      {#if result.ICD11_TM2_Code}
        <div>
          <p class="font-mono text-green-800 bg-green-200 rounded px-2 py-1 inline-block">{result.ICD11_TM2_Code}</p>
          <p class="text-xs text-gray-500 mt-1">ICD-11 (Traditional Medicine)</p>
        </div>
      {/if}
    </div>
  </div>
</div>
