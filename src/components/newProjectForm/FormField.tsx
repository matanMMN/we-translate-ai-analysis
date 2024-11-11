import { FormField, FormItem, FormLabel, FormControl, FormMessage } from "@/components/ui/form"
import { UseFormReturn } from "react-hook-form"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

interface FormFieldProps {
  form: UseFormReturn
  name: string
  label?: string
  placeholder?: string
  type?: 'input' | 'textarea' | 'select'
  options?: { value: string; label: string }[]
  className?: string
}

export function CustomFormField({
  form,
  name,
  label,
  placeholder,
  type = 'input',
  options = [],
  className = ''
}: FormFieldProps) {
  return (
    <FormField
      control={form.control}
      name={name}
      render={({ field }) => (
        <FormItem className={className}>
          {label && <FormLabel>{label}</FormLabel>}
          <FormControl>
            {type === 'input' && (
              <Input 
                placeholder={placeholder} 
                {...field} 
                className="bg-gray-50 border-gray-200"
              />
            )}
            {type === 'textarea' && (
              <Textarea 
                placeholder={placeholder} 
                {...field} 
                className="bg-gray-50 border-gray-200 min-h-[80px]"
              />
            )}
            {type === 'select' && (
              <Select 
                onValueChange={field.onChange} 
                defaultValue={field.value}
              >
                <SelectTrigger className="bg-gray-50 border-gray-200">
                  <SelectValue placeholder={placeholder} />
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
          </FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
  )
} 