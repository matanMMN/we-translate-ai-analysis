import {UseFormReturn} from "react-hook-form"
import {Input} from "@/components/ui/input"
import {Textarea} from "@/components/ui/textarea"
import {Select, SelectContent, SelectItem, SelectTrigger, SelectValue} from "@/components/ui/select"
import {
    ProjectFormField,
    ProjectFormItem,
    ProjectFormLabel,
    ProjectFormControl,
    ProjectFormMessage,
} from "./ProjectForm"
import {cn} from "@/lib/utils"


interface ProjectFormFieldProps {
    form: UseFormReturn
    name: string
    label?: string
    placeholder?: string
    type?: 'input' | 'textarea' | 'select'
    options?: { value: string; label: string }[]
    className?: string
    required?: boolean
}

export function CustomProjectFormField({
                                           form,
                                           name,
                                           label,
                                           placeholder,
                                           type = 'input',
                                           options = [],
                                           className = '',
                                           required = false
                                       }: ProjectFormFieldProps) {
    const error = form.formState.errors[name]
    const isFieldTouched = form.formState.touchedFields[name]

    return (
        <ProjectFormField
            control={form.control}
            name={name}
            render={({field}) => (
                <ProjectFormItem className={className}>
                    <div className="flex items-center gap-1 mb-1.5">
                        {label && (
                            <ProjectFormLabel>
                                {label}
                                {required && <span className="text-red-500 ml-0.5">*</span>}
                            </ProjectFormLabel>
                        )}
                    </div>
                    <ProjectFormControl>
                        {type === 'input' && (
                            <Input
                                placeholder={placeholder}
                                {...field}
                                className={cn(
                                    "bg-gray-50 border-gray-200  flex h-9 w-full rounded-md border border-input px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50",
                                    error && isFieldTouched && "border-red-500 focus-visible:ring-red-500"
                                )}
                                onBlur={() => {
                                    field.onBlur()
                                    form.trigger(name)
                                }}
                            />
                        )}
                        {type === 'textarea' && (
                            <Textarea
                                placeholder={placeholder}
                                {...field}
                                className={cn(
                                    "bg-gray-50 border-gray-200 min-h-[80px]",
                                    error && isFieldTouched && "border-red-500 focus-visible:ring-red-500"
                                )}
                                onBlur={() => {
                                    field.onBlur()
                                    form.trigger(name)
                                }}
                            />
                        )}
                        {type === 'select' && (
                            <Select
                                onValueChange={(value) => {
                                    field.onChange(value)
                                    form.trigger(name)
                                }}
                                defaultValue={field.value}
                                onOpenChange={(open) => {
                                    if (!open) {
                                        form.trigger(name)
                                    }
                                }}
                            >
                                <SelectTrigger
                                    className={cn(
                                        "bg-gray-50 border-gray-200",
                                        error && isFieldTouched && "border-red-500 focus-visible:ring-red-500"
                                    )}
                                >
                                    <SelectValue placeholder={placeholder}/>
                                </SelectTrigger>
                                <SelectContent>
                                    {options.map((option) => (
                                        <SelectItem key={option.value} value={option.value}>
                                            {option.label}
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        )}
                    </ProjectFormControl>
                    {error && isFieldTouched && (
                        <div className="mt-1.5">
                            <ProjectFormMessage className="text-sm text-red-500">
                                {error.message?.toString()}
                            </ProjectFormMessage>
                        </div>
                    )}
                </ProjectFormItem>
            )}
        />
    )
} 