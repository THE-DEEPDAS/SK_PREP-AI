import { Helmet } from "react-helmet";

export default function SEO({ title, description }) {

  return (
    <Helmet>
      <title>{title}</title>
      <meta name="description" content={description} />
      <meta name="keywords" content="UPSC AI, IAS Preparation, UPSC Notes, UPSC Current Affairs" />
      <meta name="author" content="UPSC Mastery" />
    </Helmet>
  );
}