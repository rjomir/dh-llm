import React from "react";
import { SelectButton } from 'primereact/selectbutton';
import { useForm, Controller } from "react-hook-form";
import { InputText } from "primereact/inputtext";
import { Button } from 'primereact/button';
import { classNames } from 'primereact/utils';

const settingsOptions = [
    { name: 'General', value: 1 },
    { name: 'Bert score', value: 2 },
    { name: 'Chainpoll', value: 3 }
];

export const Settings = () => {
  const initialState = {
    openaiKey: "",
  };

  const [selectedSettings, setSelectedSettings] = React.useState(1);
  const [loading, setLoading] = React.useState(false);
  const [initialValues, setInitialValues] = React.useState(initialState);

  const onSubmit = async (values) => {
      setLoading(true)
      console.log(values)
      const response = await fetch('http://localhost:5005/settings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            openaiKey: values.openaiKey,
        })
      })
      setLoading(false);
      const result = await response.json();
      console.log(result);
  };

  const {
    register,
    handleSubmit,
    control,
    formState: { errors }
  } = useForm({
    mode: "onTouched",
    reValidateMode: "onSubmit",
    defaultValues: initialValues
  });

  return (
      <div className="page-wrapper">
          <SelectButton value={selectedSettings} onChange={(e) => setSelectedSettings(e.value)} optionLabel="name" options={settingsOptions} />
          <div className="content">
              <form id="settings" onSubmit={handleSubmit(onSubmit)} className="flex flex-column gap-2">
                 {selectedSettings === 1 && (
                    <>
                        <Controller
                            name="openaiKey"
                            control={control}
                            render={({ field, fieldState }) => (
                                <>
                                 <label htmlFor="openaiKey">OPEN_API_KEY:</label>
                                 <InputText id={field.openaiKey} type="password" {...field} />
                                </>
                            )}
                        />
                     </>
                 )}
              </form>
          </div>
          <Button form="settings" label="Save settings" type="submit"/>
      </div>
  );
};

export default Settings
