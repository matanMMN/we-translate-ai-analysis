import React, {memo} from 'react';
import {ProjectFormItem, ProjectFormLabel, ProjectFormControl, ProjectFormMessage} from './ProjectForm';
import {Input} from '@/components/ui/input';
import {Textarea} from '@/components/ui/textarea';
import {Select, SelectContent, SelectItem, SelectTrigger, SelectValue} from '@/components/ui/select';
import {useFormContext} from 'react-hook-form';
import {cn} from '@/lib/utils';

export interface FormFieldProps {
    name: string;
    label: string;
    type: 'input' | 'textarea' | 'select';
    placeholder?: string;
    options?: Array<{ value: string; label: string }>;
    required?: boolean;
}

const FormField = memo(({
                            name,
                            label,
                            type,
                            placeholder,
                            options,
                            required
                        }: FormFieldProps) => {
    const {register, formState: {errors}, setValue, watch} = useFormContext();
    const value = watch(name);

    const renderField = () => {
        switch (type) {
            case 'textarea':
                return (
                    <Textarea
                        {...register(name)}
                        placeholder={placeholder}
                        className={cn("bg-gray-50 border-gray-200 min-h-[80px]",
                            errors[name] && "border-red-500 focus-visible:ring-red-500"
                        )}
                    />
                );
            case 'select':
                return (
                    <Select
                        onValueChange={(value) => setValue(name, value)}
                        defaultValue={value}
                    >
                        <SelectTrigger className={cn("bg-gray-50 border-gray-200",
                            errors[name] && "bg-gray-50 border-red-500 focus-visible:ring-red-500"
                        )}>
                            <SelectValue placeholder={`Select ${label}`}/>
                        </SelectTrigger>
                        <SelectContent>
                            {options?.map((option) => (
                                <SelectItem key={option.value} value={option.value}>
                                    {option.label}
                                </SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                );
            default:
                return (
                    <Input
                        {...register(name)}
                        placeholder={placeholder}
                        className={cn(
                            "bg-gray-50 border-gray-200  flex h-9 w-full rounded-md border border-input px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50",
                            errors[name] && "border-red-500 focus-visible:ring-red-500"
                        )}
                    />
                );
        }
    };

    return (
        <ProjectFormItem>
            <ProjectFormLabel>
                {label} {required && <span className="text-red-500">*</span>}
            </ProjectFormLabel>
            <ProjectFormControl>
                {renderField()}
            </ProjectFormControl>
            <div className="mt-1">
                {errors[name] && (
                    <ProjectFormMessage>
                        {errors[name]?.message as string}
                    </ProjectFormMessage>
                )}
            </div>
        </ProjectFormItem>
    );
});

FormField.displayName = 'FormField';

export default FormField; 