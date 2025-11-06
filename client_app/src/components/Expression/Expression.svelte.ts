import { sparkColumnFunctions } from "$lib/sparkColumnFunction";
import { v4 as uuidv4 } from "uuid";

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

class Expression {
  uuid: string = $state("");
  returnValueType: string = $state("");
  methodName: string = $state("");
  params: Param[] = $state([]);
  allowedInputTypes: Set<string> = $state(new Set([]));
  customInput: CustomInputType = $state("text");

  constructor(funcParams: any) {
    this.uuid = funcParams.uuid ? funcParams.uuid : "expr-" + uuidv4();
    this.methodName = funcParams.methodName;
    this.returnValueType = funcParams.returnValueType;

    this.params = funcParams.params
      ? funcParams.params
      : // @ts-ignore
        sparkColumnFunctions[this.returnValueType].exprs[this.methodName].params.map((p: any) => {
          return { name: p.name, dtype: p.type, valueField: { value: "", customInputUsed: false } };
        });

    // @ts-ignore
    this.allowedInputTypes = new Set(sparkColumnFunctions[this.returnValueType].allowedInputTypes);
    // @ts-ignore
    this.customInput = sparkColumnFunctions[this.returnValueType].customInput;
  }

  public compileParams(): string[] {
    return this.params.map((param: Param) => {
      if (param.dtype === "single_col") {
        if (param.valueField.customInputUsed && typeof param.valueField.value === "string") {
          return `'${param.valueField.value}'`;
        } else {
          return `${param.valueField.value}`;
        }
      } else if (param.dtype === "text") {
        const escapedValue = String(param.valueField.value)
          .replace(/\\/g, '\\\\') 
          .replace(/'/g, "''");
        return `'${escapedValue}'`;
      } else if (param.dtype === "multi_col" && param.valueField.value instanceof Array) {
        return `${param.valueField.value.join(",")}`;
      } else {
        return `${param.valueField.value}`;
      }
    });
  }
}

export class AddColumnExpression extends Expression {
  newColumnName: string = $state("");

  constructor(funcParams: any) {
    super(funcParams);
    this.newColumnName = funcParams.newColumnName ? funcParams.newColumnName : "some_column_name";
  }

  public clone(): AddColumnExpression {
    return new AddColumnExpression({
      methodName: $state.snapshot(this.methodName),
      returnValueType: $state.snapshot(this.returnValueType),
      params: $state.snapshot(this.params),
      newColumnName: $state.snapshot(this.newColumnName),
    });
  }

  public toString(): string {
    const params = this.compileParams();
    return `${this.methodName}(${params.join(", ")}) as ${this.newColumnName}`;
  }

  public pack(): any {
    return {
      expression: {
        method_name: this.methodName,
        return_value_type: this.returnValueType,
        params: this.params.map((param) => {
          return {
            ...param,
            value_json: JSON.stringify(param.valueField),
          };
        }),
        compiled: this.toString(),
      },
      new_column_name: this.newColumnName,
    };
  }
}
