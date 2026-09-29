import { apply } from "test-adapter";
export interface Input { value: number }
export function calculate(input: Input): number { return apply(input.value) + 1; }
