import React from 'react';
import { SelectButton } from 'primereact/selectbutton';
import { useForm, Controller } from 'react-hook-form';
import { InputText } from 'primereact/inputtext';
import { Button } from 'primereact/button';
import { ProgressSpinner } from 'primereact/progressspinner';
import { settingsTabs, settings, defaultFormState } from '../config.js';

export const Settings = () => {
  const [selectedSettings, setSelectedSettings] = React.useState(
    settingsTabs[0],
  );
  const [loading, setLoading] = React.useState(false);

  const { handleSubmit, control, reset } = useForm({
    mode: 'onTouched',
    reValidateMode: 'onSubmit',
    defaultValues: defaultFormState(),
  });

  React.useEffect(() => {
    const fetchData = async () => {
      const response = await fetch(`http://localhost:5005/settings`);
      const result = await response.json();
      reset(result.content);
    };

    fetchData();
  }, [reset]);

  const onSubmit = async (values) => {
    setLoading(true);
    console.log(values);
    delete values['id'];
    const response = await fetch('http://localhost:5005/settings', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        content: values,
      }),
    });
    await response.json();
    setTimeout(() => {
      setLoading(false);
    }, 2000);
  };

  return (
    <div className="page-wrapper">
      <SelectButton
        value={selectedSettings.value}
        onChange={(e) => {
          setSelectedSettings(settingsTabs[e.value]);
        }}
        optionLabel="name"
        options={settingsTabs}
      />
      <div className="content">
        <form
          id="settings"
          onSubmit={handleSubmit(onSubmit)}
          className="flex flex-column gap-2"
        >
          {settings[selectedSettings.name].map((f) => {
            return (
              <Controller
                key={f.name}
                name={f.name}
                control={control}
                render={({ field, fieldState }) => (
                  <>
                    <label htmlFor={f.name}>{f.name}:</label>
                    <InputText
                      id={field[f.name]}
                      type={f.secret ? 'password' : 'text'}
                      {...field}
                    />
                  </>
                )}
              />
            );
          })}
        </form>
      </div>
      <Button form="settings" type="submit">
        {loading ? (
          <ProgressSpinner
            style={{ width: '20px', height: '20px' }}
            strokeWidth="8"
            animationDuration=".5s"
          />
        ) : (
          'Save settings'
        )}
      </Button>
    </div>
  );
};

export default Settings;
