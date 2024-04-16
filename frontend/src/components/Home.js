import React from 'react';

import { MultiSelect } from 'primereact/multiselect';
import { InputTextarea } from 'primereact/inputtextarea';
import { ProgressSpinner } from 'primereact/progressspinner';
import { Button } from 'primereact/button';
import { classNames } from 'primereact/utils';
import { useForm, Controller } from 'react-hook-form';
import { ScoreTable } from './ScoreTable';
import { methodOptions } from '../constants';

export function Home() {
  const initState = {
    method: null,
    question: '',
    answer: '',
  };

  const [scoreLoading, setScoreLoading] = React.useState(false);
  const [scoreData, setScoreData] = React.useState();

  const onSubmit = async (values) => {
    setScoreLoading(true);
    const response = await fetch('http://localhost:5005/score', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        dataset: [
          {
            question: getValues('question'),
            answer: getValues('answer'),
            context: '',
          },
        ],
        methods: values.method,
      }),
    });
    setScoreLoading(false);
    const result = await response.json();
    setScoreData(result);
  };

  const getFormErrorMessage = (name) => {
    return (
      errors[name] && <small className="p-error">{errors[name].message}</small>
    );
  };

  const {
    handleSubmit,
    getValues,
    control,
    formState: { errors },
  } = useForm({
    mode: 'onTouched',
    reValidateMode: 'onSubmit' | 'onChange',
    defaultValues: initState,
  });

  return (
    <div className="page-wrapper">
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="flex flex-column gap-2"
      >
        <Controller
          name="method"
          control={control}
          rules={{ required: 'Method is required.' }}
          render={({ field, fieldState }) => (
            <>
              <label
                htmlFor="method"
                className={classNames({ 'p-error': errors.method })}
              >
                Select method:
              </label>
              <MultiSelect
                id={field.name}
                name="value"
                value={field.value}
                options={methodOptions}
                onChange={(e) => field.onChange(e.value)}
                optionLabel="label"
                placeholder="Select a method"
                maxSelectedLabels={3}
              />
              {getFormErrorMessage('method')}
            </>
          )}
        />
        <Controller
          name="question"
          control={control}
          rules={{ required: 'Question is required.' }}
          render={({ field, fieldState }) => (
            <>
              <label
                htmlFor="question"
                className={classNames({ 'p-error': errors.question })}
              >
                Question:
              </label>
              <InputTextarea
                id={field.question}
                {...field}
                rows={4}
                cols={30}
                className={classNames({ 'p-invalid': fieldState.invalid })}
              />
              {getFormErrorMessage('question')}
            </>
          )}
        />
        <Controller
          name="answer"
          control={control}
          render={({ field, fieldState }) => (
            <>
              <label htmlFor="answer">Answer (optional):</label>
              <InputTextarea id={field.answer} rows={4} cols={30} {...field} />
            </>
          )}
        />
        <Button label="Evaluate" type="submit" />
      </form>
      {scoreLoading && (
        <div className="flex justify-content-center">
          <ProgressSpinner
            style={{ width: '50px', height: '50px', marginTop: '20px' }}
            strokeWidth="8"
            fill="var(--surface-ground)"
            animationDuration=".5s"
          />
        </div>
      )}
      <div style={{ marginTop: '40px' }} />
      {!scoreLoading && scoreData && <ScoreTable data={scoreData} />}
    </div>
  );
}
