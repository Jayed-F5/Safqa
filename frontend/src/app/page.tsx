import styles from "./page.module.css";
import UploadForm from "./components/UploadForm";

export default function Home() {
  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <UploadForm />
      </main>
    </div>
  );
}
