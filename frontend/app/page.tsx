import ResumeUpload from "@/components/ResumeUpload";
import JobUrlForm from "@/components/JobUrlForm";

export default function Home() {
  return (
    <main className="mx-auto mt-20 max-w-2xl space-y-8">

      <ResumeUpload />

      <JobUrlForm />

    </main>
  );
}