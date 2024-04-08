import React from "react";

import { useForm } from "react-hook-form";

export const Settings = () => {
  const initState = {
    openaiKey: "",
  };

  const [initialValues, setInitialValues] = React.useState(initState);

  const onSubmit = (values) => {
    console.log("Values:::", values);
    console.log("Values:::", JSON.stringify(values));
  };

  const onError = (error) => {
    console.log("ERROR:::", error);
  };

  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm({
    mode: "onTouched",
    reValidateMode: "onSubmit",
    defaultValues: initialValues
  });

  return (
      <></>
  );
};

export default Settings
