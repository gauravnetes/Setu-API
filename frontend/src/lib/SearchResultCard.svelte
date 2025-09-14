<script lang="ts">
	import { goto } from '$app/navigation';
	import { selectedDiagnosis } from '$lib/store';
	import type { SearchResult } from './types';

	export let result: SearchResult;
	export let showAddButton: boolean = true; // default = show button

	function addToEmr() {
		selectedDiagnosis.set(result);
		goto('/emr');
	}
</script>

<div
	class="mb-4 rounded-2xl border border-sky-200 bg-white p-6 shadow-lg transition-all hover:border-sky-300 hover:shadow-xl"
>
	<div class="flex flex-col gap-6 md:flex-row md:items-start">
		<div class="flex-grow">
			<div class="flex items-center gap-2 mb-2">
				<span class="rounded-full bg-sky-100 px-3 py-1 text-xs font-semibold text-sky-800">
					{result.System}
				</span>
				{#if showAddButton}
					<div class="">
						<button
							on:click={addToEmr}
							class="rounded-full bg-sky-100 hover:bg-sky-300 hover:text-zinc-800 transition-colors duration-500 cursor-pointer px-5 py-3 text-xs font-semibold text-sky-800"
						>
							Add to Patient EMR
						</button>
					</div>
				{/if}
			</div>

			<h2 class="mt-2 text-2xl font-bold text-gray-800">{result.Traditional_Term}</h2>
			<p class="mt-1 font-mono text-gray-600">NAMASTE CODE : {result.NAMASTE_Code}</p>
			<p class="mb-2 mt-2 font-bold text-sky-400">{result.Modern_Name}</p>

			<span class="mt-5 text-lg font-bold text-zinc-600">Description :</span>
			<p class="font-semibold text-gray-700">{result.Description}</p>
		</div>

		<div class="w-full flex-shrink-0 rounded-xl border border-blue-200 bg-blue-50 p-4 md:w-64">
			<h3 class="mb-2 text-sm font-semibold text-gray-500">MAPPED CODES</h3>
			{#if result.ICD11_Biomedicine_Code}
				<div class="mb-2">
					<p class="inline-block rounded bg-blue-200 px-2 py-1 font-mono text-blue-800">
						{result.ICD11_Biomedicine_Code}
					</p>
					<p class="mt-1 text-xs text-gray-500">ICD-11 (Biomedicine)</p>
				</div>
			{/if}
			{#if result.ICD11_TM2_Code}
				<div>
					<p class="inline-block rounded bg-green-200 px-2 py-1 font-mono text-green-800">
						{result.ICD11_TM2_Code}
					</p>
					<p class="mt-1 text-xs text-gray-500">ICD-11 (Traditional Medicine)</p>
				</div>
			{/if}
		</div>
	</div>
</div>
