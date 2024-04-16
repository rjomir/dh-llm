import React from 'react';
import { SelectButton } from 'primereact/selectbutton';
import { useForm, Controller } from 'react-hook-form';
import { InputText } from 'primereact/inputtext';
import { Button } from 'primereact/button';
import { ProgressSpinner } from 'primereact/progressspinner';

const settingsOptions = [
  { name: 'General', value: 1 },
  { name: 'Bert score', value: 2 },
  { name: 'G-eval', value: 3 },
];

export const Settings = () => {
  const initialState = {
    openaiKey: '',
    openaiModel: '',
    openaiMaxTokens: 0,
    bertScoreSamplingNr: 0,
    gEvalSamplingNr: 0,
  };

  const [selectedSettings, setSelectedSettings] = React.useState(1);
  const [loading, setLoading] = React.useState(false);

  const { handleSubmit, control, reset } = useForm({
    mode: 'onTouched',
    reValidateMode: 'onSubmit',
    defaultValues: initialState,
  });

  React.useEffect(() => {
    const fetchData = async () => {
      const response = await fetch(`http://localhost:5005/settings`);
      const result = await response.json();
      reset(result);
    };

    fetchData();
  }, [reset]);

  const onSubmit = async (values) => {
    setLoading(true);
    delete values['id'];
    const response = await fetch('http://localhost:5005/settings', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...values,
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
        value={selectedSettings}
        onChange={(e) => setSelectedSettings(e.value)}
        optionLabel="name"
        options={settingsOptions}
      />
      <div className="content">
        <form
          id="settings"
          onSubmit={handleSubmit(onSubmit)}
          className="flex flex-column gap-2"
        >
          {selectedSettings === 1 && (
            <>
              <Controller
                name="openaiKey"
                control={control}
                render={({ field, fieldState }) => (
                  <>
                    <label htmlFor="openaiKey">OPEN_API_KEY:</label>
                    <InputText
                      id={field.openaiKey}
                      type="password"
                      {...field}
                    />
                  </>
                )}
              />
              <Controller
                name="openaiModel"
                control={control}
                render={({ field, fieldState }) => (
                  <>
                    <label htmlFor="openaiModel">OPEN_API_MODEL:</label>
                    <InputText id={field.openaiModel} {...field} />
                  </>
                )}
              />
              <Controller
                name="openaiMaxTokens"
                control={control}
                render={({ field, fieldState }) => (
                  <>
                    <label htmlFor="openaiMaxTokens">
                      OPEN_API_MAX_TOKENS:
                    </label>
                    <InputText
                      id={field.openaiMaxTokens}
                      type="number"
                      {...field}
                    />
                  </>
                )}
              />
            </>
          )}
          {selectedSettings === 2 && (
            <>
              <Controller
                name="bertScoreSamplingNr"
                control={control}
                render={({ field, fieldState }) => (
                  <>
                    <label htmlFor="bertScoreSamplingNr">
                      BERT_SCORE_SAMPLING_NUMBER:
                    </label>
                    <InputText
                      id={field.bertScoreSamplingNr}
                      type="number"
                      {...field}
                    />
                  </>
                )}
              />
            </>
          )}
          {selectedSettings === 3 && (
            <>
              <Controller
                name="gEvalSamplingNr"
                control={control}
                render={({ field, fieldState }) => (
                  <>
                    <label htmlFor="gEvalSamplingNr">
                      G_EVAL_SAMPLING_NUMBER:
                    </label>
                    <InputText
                      id={field.gEvalSamplingNr}
                      type="number"
                      {...field}
                    />
                  </>
                )}
              />
            </>
          )}
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
