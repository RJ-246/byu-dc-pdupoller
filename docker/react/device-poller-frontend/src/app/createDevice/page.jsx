import { useId } from "react";
export default function Page() {
  return <Form />;
}

export function Form() {
  return (
    <form>
      <FormElementText label="Device Name" />
      <FormElementText label="IP Address" />
    </form>
  );
}

export function FormElementText({ label }) {
  const id = useId();
  return (
    <div>
      <label htmlFor={id}>{label}</label>
      <input type="text" id={id} />
    </div>
  );
}
