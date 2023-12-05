import React from "react";
import styles from "./Login.module.scss";
import { LockOutlined, MailOutlined } from "@ant-design/icons";
import { Button, Checkbox, Form, Input } from "antd";
import { Link } from "react-router-dom";

const Login: React.FC = () => {
  const onFinish = (values: any) => {
    console.log("Received values of form: ", values);
  };

  return (
    <section className={styles.login}>
      <h3 className={styles.text}>Пожалуйста, авторизуйтесь</h3>
      <Form
        name="normal_login"
        className="login-form"
        initialValues={{ remember: true }}
        onFinish={onFinish}
      >
        <Form.Item
          name="email"
          rules={[
            { required: true, message: "Пожалуйста, введите ваш Email" },
            { type: "email", message: "Пожалуйста, введите корректный Email" },
          ]}
        >
          <Input
            prefix={<MailOutlined className="site-form-item-icon" />}
            placeholder="Введите Email"
            className={styles.inputs}
          />
        </Form.Item>
        <Form.Item
          name="password"
          rules={[{ required: true, message: "Пожалуйста, введите пароль" }]}
        >
          <Input
            prefix={<LockOutlined className="site-form-item-icon" />}
            type="password"
            placeholder="Введите пароль"
          />
        </Form.Item>
        <Form.Item>
          <Form.Item name="remember" valuePropName="checked" noStyle>
            <Checkbox>Запомнить меня на этом компьютере</Checkbox>
          </Form.Item>
        </Form.Item>

        <Form.Item className={styles.buttonContainer}>
          <Button type="primary" htmlType="submit" className={styles.button}>
            Войти
          </Button>
        </Form.Item>
        <div className={styles.actionLinksContainer}>
          <Link to="#">Сбросить пароль</Link>
          <Link to="#">Регистрация</Link>
        </div>
      </Form>
    </section>
  );
};

export default Login;
