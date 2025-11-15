import { sparkColumnFunctions } from "$lib/sparkColumnFunction";
import { v4 as uuidv4 } from "uuid";
import { exprs } from "./ExpressionLib";

export type Group = "math" | "date" | "string" | "misc" | "array" | "";
export type Selector = "multi" | "single";
export type SparkType =
  | "short"
  | "integer"
  | "long"
  | "float"
  | "double"
  | "decimal"
  | "array<.*>"
  | "date"
  | "timestamp"
  | "string";
export type InputType = "column" | "input";
export type CustomInput = "text" | "nan" | "checkbox" | "any" | "number";
export interface Arg {
  name: string;
  selector: Selector;
  type: InputType;
  spark_types: SparkType[];
  custom_input: CustomInput;
}
interface ValueField {
  value: string | number | string[] | number[];
  customInputUsed: boolean;
}
interface ArgWithValue {
  arg: Arg;
  valueField: ValueField;
}
interface ExpressionWithValue {
  doc: string;
  group: Group;
  args: ArgWithValue[];
}
export interface Expression {
  doc: string;
  group: Group;
  args: Arg[];
}

class Expression_2 implements ExpressionWithValue {
  uuid: string = $state("");
  name: string = $state("");
  doc: string = $state("");
  group: Group = $state("");
  args: ArgWithValue[] = $state([]);

  constructor(params: any) {
    this.uuid = params.uuid ? params.uuid : "expr-" + uuidv4();
    this.name = params.name;
    this.doc = params.doc ? params.doc : exprs[params.name].doc;
    this.group = params.group ? params.group : exprs[params.name].group;
    this.args = params.args
      ? params.args
      : exprs[params.name].args.map((p: Arg) => {
          const initValue = p.selector === "multi" ? [] : "";
          return { arg: { ...p }, valueField: { value: initValue, customInputUsed: false } };
        });
  }

  public compile(): string[] {
    return this.args.map((arg: ArgWithValue) => {
      if (arg.arg.selector === "single") {
        if (arg.valueField.customInputUsed && arg.arg.custom_input == "text") {
          return `'${arg.valueField.value}'`;
        } else {
          return `${arg.valueField.value}`;
        }
      } else if (arg.arg.custom_input === "text") {
        const escapedValue = String(arg.valueField.value).replace(/\\/g, "\\\\").replace(/'/g, "''");
        return `'${escapedValue}'`;
      } else if (arg.arg.selector === "multi" && arg.valueField.value instanceof Array) {
        return `${arg.valueField.value.join(",")}`;
      } else {
        return `${arg.valueField.value}`;
      }
    });
  }
}

type CustomInputType = "number" | "text";
interface ValueField {
  value: string | number | string[] | number[];
  customInputUsed: boolean;
}
interface Param {
  name: string;
  dtype: string;
  valueField: ValueField;
}

export class AddColumnExpression extends Expression_2 {
  newColumnName: string = $state("");

  constructor(funcParams: any) {
    super(funcParams);
    this.newColumnName = funcParams.newColumnName ? funcParams.newColumnName : "new_col";
  }

  public clone(): AddColumnExpression {
    return new AddColumnExpression({
      name: $state.snapshot(this.name),
      doc: $state.snapshot(this.doc),
      group: $state.snapshot(this.group),
      args: this.args.map((a) => {
        return { arg: $state.snapshot(a.arg), valueField: $state.snapshot(a.valueField) };
      }),
      newColumnName: $state.snapshot(this.newColumnName),
    });
  }

  public toString(): string {
    const compiledArgs = this.compile();
    return `${this.name}(${compiledArgs.join(", ")}) as ${this.newColumnName}`;
  }

  // public pack(): any {
  //   return {
  //     expression: {
  //       method_name: this.methodName,
  //       return_value_type: this.returnValueType,
  //       params: this.params.map((param) => {
  //         return {
  //           ...param,
  //           value_json: JSON.stringify(param.valueField),
  //         };
  //       }),
  //       compiled: this.toString(),
  //     },
  //     new_column_name: this.newColumnName,
  //   };
  // }
}
