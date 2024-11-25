export default function Errors({errors}: { errors?: string[] }) {
    return errors && errors.map(err => <p key={err} className="text-red-500 text-sm">{err}</p>);
}