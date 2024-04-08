import React from "react";

import { InputText } from "primereact/inputtext";
import { InputTextarea } from "primereact/inputtextarea";
import { Column } from 'primereact/column';
import { ScoreTable } from './ScoreTable';
import { DataTable } from 'primereact/datatable';
import { ProgressSpinner } from 'primereact/progressspinner';
import { Dropdown } from 'primereact/dropdown';
import { MultiSelect } from 'primereact/multiselect';
import { Divider } from 'primereact/divider';
import { Button } from 'primereact/button';
import { classNames } from 'primereact/utils';
import { Card } from 'primereact/card';

import { useForm, Controller } from "react-hook-form";

const datasetOptions = [{ label:'COVID-QA', value: 'covid-qa' }, { label: 'Drop', value: 'drop' }, { label:'Databricks Dolly', value: 'databricks-dolly' }]
const methodOptions = [{ label:'Bert', value: 'bert' }, { label: 'Ngram', value: 'ngram' }]

export const Benchmarks = () => {
  const initialState = {
    dataset: null,
    method: null
  };

  const [initialValues, setInitialValues] = React.useState(initialState);
  const [selected, setSelected] = React.useState([]);
  const [datasetLoaded, setDatasetLoaded] = React.useState(false)
  const [loading, setLoading] = React.useState(false)
  const [datasetSelected, setDatasetSelected] = React.useState(null)
  const [benchmarkData, setBenchmarkData] = React.useState([]);
  const [selectedRows, setSelectedRows] = React.useState([]);
  const [selectAll, setSelectAll] = React.useState(false);
  const [scoreLoading, setScoreLoading] = React.useState(false);
  const [scoreData, setScoreData] = React.useState();

  React.useEffect(() => {
    const fetchData = async () => {
        setLoading(true);
        const response = await fetch(`http://localhost:5005/benchmark/${datasetSelected}`);
        const result = await response.json();
        console.log(result)
        setBenchmarkData(result);
        setLoading(false);
        setDatasetLoaded(true);
    }

    if(datasetSelected){
        setBenchmarkData([]);
        fetchData();
    }
  }, [datasetSelected])

  const onSubmit = async (values) => {
      setScoreLoading(true)
      const response = await fetch('http://localhost:5005/score', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            dataset: selectAll ? benchmarkData : selectedRows,
            methods: values.method
        })
      })
      setScoreLoading(false);
      const result = await response.json();
      setScoreData(result);
  };

  const {
    register,
    handleSubmit,
    control,
    setError,
    clearErrors,
    formState: { errors, isSubmitting }
  } = useForm({
    mode: "onTouched",
    reValidateMode: "onSubmit" | "onChange",
    defaultValues: initialValues
  });

  React.useEffect(() => {
    if(isSubmitting && (selectedRows.length < 1 && !selectAll)) {
        setError("selectedRows", {
          type: "manual",
          message: "Dataset rows should be selected!",
        })
    }
  }, [isSubmitting, setError, selectedRows, selectAll])

  const getFormErrorMessage = (name) => {
    return errors[name] && <small className="p-error">{errors[name].message}</small>
  };

  return (
    <div className="page-wrapper">
      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-column gap-2">
            <Controller
                name="dataset"
                control={control}
                rules={{ required: 'Dataset is required.' }}
                render={({ field, fieldState }) => (
                    <>
                        <label htmlFor="dataset" className={classNames({ 'p-error': errors.dataset })}>Select dataset:</label>
                        <Dropdown
                            id={field.name}
                            value={field.value}
                            optionLabel="label"
                            placeholder="Select a Dataset"
                            options={datasetOptions}
                            focusInputRef={field.ref}
                            onChange={(e) => {
                                    clearErrors("selectedRows")
                                    setDatasetSelected(e.value)
                                    field.onChange(e.value)
                                }
                            }
                            className={classNames({ 'p-invalid': fieldState.error })}
                        />
                        {getFormErrorMessage('dataset')}
                    </>
                )}
            />
            {loading && (
                <div className="flex justify-content-center">
                   <ProgressSpinner style={{width: '50px', height: '50px', marginTop: '20px'}} strokeWidth="8" fill="var(--surface-ground)" animationDuration=".5s" />
                </div>
            )}
            {datasetLoaded && (
                <DataTable
                    value={benchmarkData}
                    scrollable
                    scrollHeight="400px"
                    virtualScrollerOptions={{ itemSize: 46 }}
                    selectionMode={'checkbox'}
                    onSelectAllChange={(e) => {
                        const checked = e.checked
                        if(checked) {
                            clearErrors("selectedRows")
                        }
                        setSelectAll(e.checked)}
                    }
                    selection={selectedRows}
                    onSelectionChange={(e) => {
                        clearErrors("selectedRows")
                        setSelectedRows(e.value)}
                    }
                    isDataSelectable={() => !selectAll}
                    selectAll={selectAll}
                    tableStyle={{ minWidth: '50rem' }}>
                        <Column selectionMode="multiple" headerStyle={{ width: '3rem' }} />
                        <Column style={{ width: '25%' }} field="question" header="Question" />
                        <Column style={{ width: '55%' }} field="answer" header="Answer" />
                        <Column style={{ width: '25%' }} field="category" header="Category" />
                </DataTable>)
            }
            {getFormErrorMessage('selectedRows')}
            <div style={{ marginTop: "25px" }} />
            <Controller
                name="method"
                control={control}
                rules={{ required: 'Method is required.' }}
                render={({ field, fieldState }) => (
                    <>
                        <label htmlFor="method" className={classNames({ 'p-error': errors.method })}>Select method:</label>
                        <MultiSelect
                            id={field.name}
                            name="value"
                            value={field.value}
                            options={methodOptions}
                            onChange={(e) => field.onChange(e.value)}
                            optionLabel="label"
                            placeholder="Select a method"
                            maxSelectedLabels={3} />
                        {getFormErrorMessage('method')}
                    </>
                )}
            />
            <div style={{ marginTop: "40px" }} />
         <Button label="Submit" type="submit"/>
      </form>
      {scoreLoading && (
        <div className="flex justify-content-center">
           <ProgressSpinner style={{width: '50px', height: '50px', marginTop: '20px'}} strokeWidth="8" fill="var(--surface-ground)" animationDuration=".5s" />
        </div>
      )}
      <div style={{ marginTop: "40px" }} />
      {!scoreLoading && scoreData && (
        <ScoreTable data={scoreData} />
      )}
    </div>
  );
};

