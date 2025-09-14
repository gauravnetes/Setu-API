import { writable } from 'svelte/store';
import type { SearchResult } from './types';

// This store will hold the diagnosis we select to add to the EMR
export const selectedDiagnosis = writable<SearchResult | null>(null);